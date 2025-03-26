import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
import tkinter as tk

def gerar_voronoi(num_pontos, largura, altura):
    """Gera um diagrama de Voronoi.

    Args:
        num_pontos (int): O número de pontos (sementes) para o diagrama.
        largura (int): A largura da área do diagrama.
        altura (int): A altura da área do diagrama.

    Returns:
        scipy.spatial.Voronoi: O objeto Voronoi gerado.
    """
    # Gerar pontos aleatórios dentro das dimensões especificadas
    pontos = np.random.rand(num_pontos, 2) * [largura, altura]
    # Gerar o diagrama de Voronoi
    vor = Voronoi(pontos)
    return vor

def desenhar_voronoi(canvas, voronoi, largura, altura, cores):
    """Desenha o diagrama de Voronoi em um canvas do Tkinter.

    Args:
        canvas (tk.Canvas): O canvas do Tkinter onde o diagrama será desenhado.
        voronoi (scipy.spatial.Voronoi): O objeto Voronoi a ser desenhado.
        largura (int): A largura da área do diagrama.
        altura (int): A altura da área do diagrama.
        cores (list): Uma lista de cores para as células do Voronoi.
    """
    # Limpar o canvas
    canvas.delete("all")

    # Desenhar o fundo branco
    canvas.create_rectangle(0, 0, largura, altura, fill="white", outline="")

    # Desenhar as regiões do Voronoi
    for region in voronoi.regions:
        if not -1 in region and len(region) > 0:
            polygon = [tuple(voronoi.vertices[i]) for i in region]
            # Reduzir o tamanho do polígono para criar um espaço entre as células
            centro_x = sum(p[0] for p in polygon) / len(polygon)
            centro_y = sum(p[1] for p in polygon) / len(polygon)
            novo_polygon = []
            for x, y in polygon:
                dx = x - centro_x
                dy = y - centro_y
                distancia = max(abs(dx), abs(dy)) #usando o maior valor para manter a proporcao
                if distancia > 0:
                    fator_reducao = 0.85  # Ajuste este valor para controlar o espaço entre as células - AUMENTADO PARA 0.85
                    novo_x = centro_x + dx * fator_reducao
                    novo_y = centro_y + dy * fator_reducao
                    novo_polygon.append((novo_x, novo_y))
                else:
                    novo_polygon.append((x,y))
            # Desenhar o polígono no canvas
            canvas.create_polygon(novo_polygon, fill="black", outline="#EEEEEE", smooth=True, width=1)

    # Desenhar os pontos (sementes)
    for ponto in voronoi.points:
        x, y = ponto
        canvas.create_oval(x - 1, y - 1, x + 1, y + 1, fill="black", outline="")
