import OpenGL

OpenGL.ERROR_ON_COPY = True
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# PyOpenGL 3.0.1 introduces this convenience module...
from OpenGL.GL.shaders import *
import numpy as np
from PIL import Image

import sys

program = None


def InitGL(Width, Height, texture_image):
    # set background pixels
    glClearColor(0.0, 0.0, 0.0, 0.0)

    # up to 8 textures in one time
    glBindTexture(GL_TEXTURE_2D, 0)

    # set texture context
    glTexImage2D(GL_TEXTURE_2D,
                 0,
                 GL_RGB,
                 texture_image.size[0],
                 texture_image.size[1],
                 0,
                 GL_RGBA,
                 GL_UNSIGNED_BYTE,
                 np.array(list(texture_image.getdata()), np.uint8))

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

    # Set Camera Matrix parameters
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, window_width / window_height, 0.01, 100.0)

    # set ModelView Matrix parameters
    glMatrixMode(GL_MODELVIEW)

    global program
    # Compile Shaders, Link to GL-program, compile Program
    program = compileProgram(
        compileShader('''
            varying vec2 pos;
            uniform float texture_width;
            uniform float texture_height;

            void main() {

                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                pos = gl_MultiTexCoord0.st;

            }
        ''', GL_VERTEX_SHADER),
        compileShader('''
            varying vec2 pos;
            uniform sampler2D s_texture;
            uniform float texture_width;
            uniform float texture_height;


            void main(void) 
            {
	            vec4 n[9];
	            float w = 1.0 / texture_width;
	            float h = 1.0 / texture_height;
                vec2 coord = pos.xy;

	            n[0] = texture2D(s_texture, coord + vec2( -w, -h));
	            n[1] = texture2D(s_texture, coord + vec2(0.0, -h));
	            n[2] = texture2D(s_texture, coord + vec2(  w, -h));
	            n[3] = texture2D(s_texture, coord + vec2( -w, 0.0));
	            n[4] = texture2D(s_texture, coord);
	            n[5] = texture2D(s_texture, coord + vec2(  w, 0.0));
	            n[6] = texture2D(s_texture, coord + vec2( -w, h));
	            n[7] = texture2D(s_texture, coord + vec2(0.0, h));
	            n[8] = texture2D(s_texture, coord + vec2(  w, h));

	            vec4 G_x = n[8] - n[4];
  	            vec4 G_y = n[7] - n[5];
	            vec4 roberts = sqrt((G_x * G_x) + (G_y * G_y));
                float R = roberts.r;
                float G = roberts.g;
                float B = roberts.b;
                float L = (R + G + B) / 3;
	            gl_FragColor = vec4(L, L, L, 1.0);
            }
    ''', GL_FRAGMENT_SHADER), )


def DrawGLScene():
    # Clear color buffer
    glClear(GL_COLOR_BUFFER_BIT)

    # Restore Model Matrix parameters
    glLoadIdentity()

    # Translate
    glTranslatef(0, 0, -7)

    # Load OpenGL(with shaders)program context
    glUseProgram(program)

    # Texture
    glEnable(GL_TEXTURE_2D)
    #glEnable(GL_FRAMEBUFFER_SRGB)
    # Draw Quad-points with associated texture coordinates

    glBegin(GL_QUADS)
    glVertex3f(-5, -5, 0)
    glTexCoord2f(0, 0)

    glVertex3f(-5, 5, 0)
    glTexCoord2f(0, 1)

    glVertex3f(5, 5, 0)
    glTexCoord2f(1, 1)

    glVertex3f(5, -5, 0)
    glTexCoord2f(1, 0)
    glEnd()

    # Load parameters to fragment shader
    glUniform1i(glGetUniformLocation(program, "s_texture"), 0);
    glUniform1f(glGetUniformLocation(program, "texture_width"), float(texture_image.size[0]))
    glUniform1f(glGetUniformLocation(program, "texture_height"), float(texture_image.size[1]))

    glFlush()


global window
glutInit(sys.argv)

texture_image = Image.open('картинка.jpg').convert('RGBA').rotate(90)
window_width, window_height = texture_image.size

glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(0, 0)
window = glutCreateWindow("Roberts_GPU")

glutDisplayFunc(DrawGLScene)
glutIdleFunc(DrawGLScene)

InitGL(window_width, window_height, texture_image)

glutMainLoop()