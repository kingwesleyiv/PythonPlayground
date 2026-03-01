import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
from mss import mss
import ctypes

# ---------- CONFIG ----------
DISPLAY_SCALE = 0.5
FPS = 60
BLUR_RADIUS = 10      # number of texel offsets
# ----------------------------

# Vertex Shader (common)
VERTEX_SHADER = """
#version 330
in vec2 position;
in vec2 texcoord;
out vec2 v_texcoord;
void main()
{
    v_texcoord = texcoord;
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

# Fragment Shader for single blur pass
FRAGMENT_SHADER = """
#version 330
in vec2 v_texcoord;
out vec4 fragColor;

uniform sampler2D screenTex;
uniform vec2 texOffset;

void main()
{
    vec3 result = texture(screenTex, v_texcoord).rgb * 0.227027;

    result += texture(screenTex, v_texcoord + texOffset * 1.384615).rgb * 0.316216;
    result += texture(screenTex, v_texcoord - texOffset * 1.384615).rgb * 0.316216;

    result += texture(screenTex, v_texcoord + texOffset * 3.230769).rgb * 0.070270;
    result += texture(screenTex, v_texcoord - texOffset * 3.230769).rgb * 0.070270;

    fragColor = vec4(result, 1.0);
}
"""

# Shader helpers
def compile_shader(src, type_):
    shader = glCreateShader(type_)
    glShaderSource(shader, src)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader))
    return shader

def create_program(vs_src, fs_src):
    vs = compile_shader(vs_src, GL_VERTEX_SHADER)
    fs = compile_shader(fs_src, GL_FRAGMENT_SHADER)
    program = glCreateProgram()
    glAttachShader(program, vs)
    glAttachShader(program, fs)
    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program))
    glDeleteShader(vs)
    glDeleteShader(fs)
    return program

# Pygame + OpenGL init
pygame.init()
with mss() as sct:
    monitor = sct.monitors[1]
    SCREEN_WIDTH = monitor["width"]
    SCREEN_HEIGHT = monitor["height"]

WIN_WIDTH = int(SCREEN_WIDTH * DISPLAY_SCALE)
WIN_HEIGHT = int(SCREEN_HEIGHT * DISPLAY_SCALE)
pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), DOUBLEBUF | OPENGL)
pygame.display.set_caption("GPU 2-Pass Blur")

# Fullscreen quad
vertices = np.array([
    -1.0, -1.0,  0.0, 0.0,
     1.0, -1.0,  1.0, 0.0,
    -1.0,  1.0,  0.0, 1.0,
     1.0,  1.0,  1.0, 1.0,
], dtype=np.float32)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

def set_vertex_attribs(program):
    pos = glGetAttribLocation(program, "position")
    tex = glGetAttribLocation(program, "texcoord")
    glEnableVertexAttribArray(pos)
    glVertexAttribPointer(pos, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
    glEnableVertexAttribArray(tex)
    glVertexAttribPointer(tex, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))

# Shaders
h_prog = create_program(VERTEX_SHADER, FRAGMENT_SHADER)  # Horizontal
v_prog = create_program(VERTEX_SHADER, FRAGMENT_SHADER)  # Vertical
set_vertex_attribs(h_prog)

# Textures
texA = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texA)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

texB = glGenTextures(1)
glBindTexture(GL_TEXTURE_2D, texB)
# Allocate empty GPU texture once
glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, WIN_WIDTH, WIN_HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Framebuffer (attach once)
fbo = glGenFramebuffers(1)
glBindFramebuffer(GL_FRAMEBUFFER, fbo)
glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texB, 0)
status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
if status != GL_FRAMEBUFFER_COMPLETE:
    raise RuntimeError(f"Framebuffer incomplete: {status}")
glBindFramebuffer(GL_FRAMEBUFFER, 0)  # unbind

clock = pygame.time.Clock()

with mss() as sct:
    monitor_region = {"top":0, "left":0, "width":SCREEN_WIDTH, "height":SCREEN_HEIGHT}

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        # Screen capture
        raw = sct.grab(monitor_region)
        frame = np.array(raw)[:, :, :3][:, :, ::-1]  # BGR → RGB
        frame = frame[::int(1/DISPLAY_SCALE), ::int(1/DISPLAY_SCALE)]

        # Upload to texA
        glBindTexture(GL_TEXTURE_2D, texA)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, WIN_WIDTH, WIN_HEIGHT, 0, GL_RGB, GL_UNSIGNED_BYTE, frame)

        # ----- Horizontal pass -----
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        glViewport(0, 0, WIN_WIDTH, WIN_HEIGHT)
        glUseProgram(h_prog)
        glUniform2f(glGetUniformLocation(h_prog, "texOffset"), BLUR_RADIUS / WIN_WIDTH, 0.0)
        glBindTexture(GL_TEXTURE_2D, texA)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        # ----- Vertical pass -----
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glViewport(0, 0, WIN_WIDTH, WIN_HEIGHT)
        glUseProgram(v_prog)
        glUniform2f(glGetUniformLocation(v_prog, "texOffset"), 0.0, BLUR_RADIUS / WIN_HEIGHT)
        glBindTexture(GL_TEXTURE_2D, texB)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

        pygame.display.flip()
        clock.tick(FPS)
        print("FPS:", round(clock.get_fps()))

pygame.quit()