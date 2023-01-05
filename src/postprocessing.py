"""
Shader code adapted from https://github.com/hiulit/Godot-3-2D-CRT-Shader/blob/master/crt_shader.shader:

MIT License

Copyright (c) 2019 Xavier Gómez Gosálbez (a.k.a. hiulit)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import pygame

from functools import wraps

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *
import ctypes
import glm

render_surface = None
display_surface = None
surface_texture = None
post_processing_program = None
screen_size = (0,0)
shader_code = (
"""
#version 300 es
precision mediump float;

layout (location = 0) in vec3 a_pos;
layout (location = 1) in vec2 a_uv;

out vec2 v_uv;

void main()
{
    v_uv = a_uv;
    gl_Position = vec4(a_pos.xyz, 1.0);
}
""",
"""
#version 300 es
precision mediump float;

out vec4 frag_color;
in vec2 v_uv;

uniform sampler2D u_frame;

vec2 crt_uv(vec2 uv)
{
    uv = uv * 2.0 - 1.0;
    vec2 offset = abs(uv.yx) / vec2(6.0, 6.0);
    uv = uv + uv * offset * offset;
    uv = uv * 0.5 + 0.5;
    return uv;
}

void main()
{
    vec2 new_uv = crt_uv(v_uv);
    vec3 color = texture(u_frame, new_uv).rgb;
    
    float s = sin(new_uv.y * 240.0 * 3.1415 * 2.0);
    s = (s * 0.5 + 0.5) * 0.9 + 0.1;
    color = color * vec3(s);
    
    if (new_uv.x < 0.0 || new_uv.x > 1.0 || new_uv.y < 0.0 || new_uv.y > 1.0)
    {
        color = vec3(0.0, 0.0, 0.0);
    }
    
    frag_color = vec4(color.rgb, 1.0);
}"""
)

def patch_init(func):
	@wraps(func)
	def init_wrapper(*args, **kwargs):
		global screen_size
		func(*args, **kwargs)
		screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		print(screen_size)
	return init_wrapper
	
def patch_display_get_surface(func):
	@wraps(func)
	def get_surface_wrapper(*args, **kwargs):
		global display_surface
		return display_surface
	return get_surface_wrapper

def patch_display_set_mode(func):
	@wraps(func)
	def set_mode_wrapper(*args, **kwargs):
		global render_surface
		global display_surface
		global surface_texture
		global post_processing_program
		global shader_code
		global quad_vao
		global screen_size
		
		requested_size = args[0]
		args = list(args)
		args[0] = screen_size
		args = tuple(args)
		
		if "flags" in kwargs or len(args) == 1:
			kwargs["flags"] = pygame.FULLSCREEN | pygame.OPENGL
		else:
			args = list(args)
			args[1] = pygame.FULLSCREEN | pygame.OPENGL
			args = tuple(args)
				
		render_surface = func(*args, **kwargs)
		display_surface = pygame.Surface(requested_size)
		
		surface_texture = glGenTextures(1)
		glBindTexture(GL_TEXTURE_2D, surface_texture)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, requested_size[0], requested_size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glBindTexture(GL_TEXTURE_2D, 0)
		
		post_processing_program = compileProgram(compileShader(shader_code[0], GL_VERTEX_SHADER), compileShader(shader_code[1], GL_FRAGMENT_SHADER))
		
		v = [(-1,-1,0), (1,-1,0), (1,1,0), (-1,1,0)]
		uv = [(0,1), (1,1), (1,0), (0,0),]
		surfaces = [(0,1,2,3)]

		face_attributes = []
		for i, quad in enumerate(surfaces):
			for iv in quad:
				face_attributes += v[iv]
				face_attributes += uv[iv]

		face_vbos = glGenBuffers(1)
		glBindBuffer(GL_ARRAY_BUFFER, face_vbos)
		glBufferData(GL_ARRAY_BUFFER, (GLfloat * len(face_attributes))(*face_attributes), GL_STATIC_DRAW)
		quad_vao = glGenVertexArrays(1)
		glBindVertexArray(quad_vao)
		glVertexAttribPointer(0, 3, GL_FLOAT, False, 5*ctypes.sizeof(GLfloat), ctypes.c_void_p(0)) 
		glEnableVertexAttribArray(0)
		glVertexAttribPointer(1, 2, GL_FLOAT, False, 5*ctypes.sizeof(GLfloat), ctypes.c_void_p(3*ctypes.sizeof(GLfloat))) 
		glEnableVertexAttribArray(1) 
		
		return display_surface
	return set_mode_wrapper
	
def patch_display_flip(func):
	@wraps(func)
	def flip_wrapper(*args, **kwargs):
		global render_surface
		global display_surface
		global surface_texture
		global post_processing_program
		global quad_vao
		
		surface_texture_bytes = pygame.image.tostring(display_surface, "RGB")
		
		glBindFramebuffer(GL_FRAMEBUFFER, 0)
		glClearColor(0.0, 0.0, 1, 1)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glUseProgram(post_processing_program)
		glBindTexture(GL_TEXTURE_2D, surface_texture)
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, display_surface.get_width(), display_surface.get_height(), 0, GL_RGB, GL_UNSIGNED_BYTE, surface_texture_bytes)
		glViewport(0,0, render_surface.get_width(), render_surface.get_height())
		
		glBindVertexArray(quad_vao)
		glDrawArrays(GL_QUADS, 0, 4)
		glBindVertexArray(0)
		
		return func(*args, **kwargs)
	return flip_wrapper
	
def patch_display_update(func):
	@wraps(func)
	def udate_wrapper(*args, **kwargs):
		return pygame.display.flip()
	return udate_wrapper
	

pygame.init = patch_init(pygame.init)
pygame.display.set_mode = patch_display_set_mode(pygame.display.set_mode)
pygame.display.flip = patch_display_flip(pygame.display.flip)
pygame.display.update = patch_display_update(pygame.display.update)
pygame.display.get_surface = patch_display_get_surface(pygame.display.get_surface)
