import pygame
import numpy
import random
from pygame.constants import K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_SPACE, K_UP, K_a, K_d, K_s, K_w
from model import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glm

pygame.init()
screen = pygame.display.set_mode((1200, 720), pygame.OPENGL | pygame.DOUBLEBUF)
glClearColor(1, 1, 1, 1.0)
glEnable(GL_DEPTH_TEST)
clock = pygame.time.Clock()

vertex_shader = """
#version 460

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;

uniform mat4 theMatrix;
uniform vec3 light;

out vec2 vertexTexcoords;
out float intensity;
out vec3 mycolor;
out vec3 pos;

void main() 
{
  intensity = dot(normal, normalize(light - position));
  if (intensity < 0.4) {
    intensity = intensity + 0.5;
  }
  gl_Position = theMatrix * vec4(position.x, position.y, position.z, 1);
  mycolor = normal;
  pos = position;
}
"""
shader="""
#version 460
layout(location = 0) out vec4 fragColor;

uniform int clock;
uniform int cont;
uniform float randNumber1;
uniform float randNumber2;
uniform float randNumber3;
uniform int oscilador;
in vec3 mycolor;
in float intensity;
in vec3 pos;



void main()
{
  if(cont == 0) {
    if((pos.z > 0 && pos.z < 15) || (pos.z > 25 && pos.z < 40) || (pos.z < -20 && pos.z > -35) || (pos.z < -40 && pos.z > -50 || (pos.z < -60 && pos.z > -70))){
      fragColor = vec4(0.35f, 0.23f, 0.12f, 1.0f)*intensity;
    }
    else {
      fragColor = vec4(1.0f, 1.0f, 0.0f, 1.0f)*intensity;
    }
  }
  else if(cont == 1) {
    if (oscilador == 0) {
      fragColor = vec4(1.0f - mod(clock,50) / 50, 0.0f, 1.0f- mod(clock,50) / 50, 1.0f) * intensity;
    }
    else {
      fragColor = vec4(0.0f + mod(clock,50) / 50, 0.0f, 0.0f + mod(clock,50) / 50, 1.0f) * intensity;
    }
  }
  else if(cont == 2) {
    fragColor = vec4(randNumber1, randNumber2, randNumber3, 1.0f) * intensity;
  }
  
}

"""

cvs = compileShader(vertex_shader, GL_VERTEX_SHADER)
cfs = compileShader(shader, GL_FRAGMENT_SHADER)

shader = compileProgram(cvs, cfs)

mesh = Obj('./fox.obj')

if len(mesh.normals)<len(mesh.vertices):
  faltante = len(mesh.vertices)-len(mesh.normals)
  for i in range(faltante):
    mesh.normals.append([0.0,0.0,1.0])
if len(mesh.normals)>len(mesh.vertices):
  faltante = len(mesh.normals)-len(mesh.vertices)
  for i in range(faltante):
    mesh.vertices.append([0.0,0.0,0.0])

vertex_data = numpy.hstack((
  numpy.array(mesh.vertices, dtype=numpy.float32),
  numpy.array(mesh.normals, dtype=numpy.float32),
)).flatten()


index_data = numpy.array([[vertex[0] for vertex in face] for face in mesh.vfaces], dtype=numpy.uint32).flatten()
print(index_data)
vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)
glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)
glVertexAttribPointer(
  0, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(0)
)
glEnableVertexAttribArray(0)

element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(
  1, # location
  3, # size
  GL_FLOAT, # tipo
  GL_FALSE, # normalizados
  4 * 6, # stride
  ctypes.c_void_p(4 * 3)
)
glEnableVertexAttribArray(1)

glUseProgram(shader)
def render(right, up, forward, rotate):
  i = glm.mat4(1)
  translate = glm.translate(i, glm.vec3(0, 0, 0))
  rotate = glm.rotate(i, glm.radians(rotate), glm.vec3(0, 1, 0))
  scale = glm.scale(i, glm.vec3(0.5, 0.5, 0.5))

  model = translate * rotate * scale
  view = glm.lookAt(glm.vec3(right, up, forward), glm.vec3(0.0, 1.0, 0.0), glm.vec3(0, 1, 0))
  projection = glm.perspective(glm.radians(45), 1200/720, 0.1, 1000.0)

  theMatrix = projection * view * model

  glUniformMatrix4fv(
    glGetUniformLocation(shader, 'theMatrix'),
    1,
    GL_FALSE,
    glm.value_ptr(theMatrix)
  )
  glUniform3f(glGetUniformLocation(shader, "light"),
                        0, 0, 10)

glViewport(0, 0, 1200, 720)

cont = 0
osc = 0
a = 0
right = 0
up = 0
forward = 20
rn1 = random.random()
rn2 = random.random()
rn3 = random.random()
rotate = 0
running = True
render(right, up, forward, rotate)
while running:
  glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

  glUniform1i(
    glGetUniformLocation(shader, 'clock'),
    a
  )
  glUniform1i(
    glGetUniformLocation(shader, 'cont'),
    cont
  )
  glUniform1f(
    glGetUniformLocation(shader, 'randNumber1'),
    rn1
  )
  glUniform1f(
    glGetUniformLocation(shader, 'randNumber2'),
    rn2
  )
  glUniform1f(
    glGetUniformLocation(shader, 'randNumber3'),
    rn3
  )
  glUniform1i(
    glGetUniformLocation(shader, 'oscilador'),
    osc
  )


  a += 1

  glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

  pygame.display.flip()
  clock.tick(15)
  pressed_keys = pygame.key.get_pressed()
  if pressed_keys[K_UP]:
    up += 5
  elif pressed_keys[K_DOWN]:
    up -= 5
  elif pressed_keys[K_LEFT]:
    right -= 5
  elif pressed_keys[K_RIGHT]:
    right += 5
  elif pressed_keys[K_a]:
    rotate -= 10
  elif pressed_keys[K_d]:
    rotate += 10
  elif pressed_keys[K_w]:
    forward -= 10
  elif pressed_keys[K_s]:
    forward += 10
  elif pressed_keys[K_ESCAPE]:
    running = False
  elif pressed_keys[K_SPACE]:
    cont = (cont + 1) % 3 
  if a % 10 == 0:
    rn1 = random.random()
    rn2 = random.random()
    rn3 = random.random()
  if a % 50 == 0:
    if osc == 1:
      osc = 0
    else:
      osc = 1
  render(right, up, forward, rotate)
  pygame.event.pump()