#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################ Graphes ##############################################

import networkx
from bokeh.io import output_notebook, show, save
from bokeh.plotting import figure
from bokeh.plotting import from_networkx
from bokeh.io import output_notebook, show, save
from bokeh.models import Range1d, Circle, ColumnDataSource, MultiLine
from bokeh.palettes import Blues8, Reds8, Purples8, Oranges8, Viridis8, Spectral8
from bokeh.transform import linear_cmap
from bokeh.models import EdgesAndLinkedNodes, NodesAndLinkedEdges
from networkx.algorithms import community

def Grap(df_graphe):
    
    G = networkx.from_pandas_edgelist(df_graphe,'source', 'target')
    
    #titre
    titre = 'Graphes des mots du corpus de documents'
    
    #On calcule un degree pour chaque Noeud et on lui assigne un attribut. Un degree est le nombre de lien qu'un noeud comporte
    degrees = dict(networkx.degree(G))
    networkx.set_node_attributes(G, name='degree', values=degrees)
    
    #La c'est pour la subrillance entre les liens et les noeuds quand on passe la souris dessus
    node_highlight_color = 'white'
    edge_highlight_color = 'black'
    
    #On ajuste les petits noeuds pour qu'ils soient toujours visible
    number_to_adjust_by = 5
    adjusted_node_size = dict([(node, degree+number_to_adjust_by) for node, degree in networkx.degree(G)])
    networkx.set_node_attributes(G, name='adjusted_node_size', values=adjusted_node_size)
    
    #Gestion des couleurs/tailles
    size_by_this_attribute = 'adjusted_node_size'
    color_by_this_attribute = 'adjusted_node_size'
    
    #La je choisie ma palette de couleur
    color_palette = Blues8
    
    #Hover pour quand on survole le noeud
    HOVER_TOOLTIPS = [("Source", "@index"),("Mot","@degree")]
    
    #Création du plot — set dimensions, toolbar, et titre
    plot = figure(tooltips = HOVER_TOOLTIPS, tools="pan,wheel_zoom,save,reset", active_scroll='wheel_zoom',x_range=Range1d(-10.1, 10.1), y_range=Range1d(-10.1, 10.1), title=titre)
    
    #Création d'un graphe
    network_graph = from_networkx(G, networkx.spring_layout, scale=10, center=(0, 0))
    
    #################################################################Ici on va pimper notre graph##################################################################
    
    #Surlignage des noeuds
    network_graph.node_renderer.hover_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    network_graph.node_renderer.selection_glyph = Circle(size=size_by_this_attribute, fill_color=node_highlight_color, line_width=2)
    
    #Opacité et épaisseur
    network_graph.edge_renderer.glyph = MultiLine(line_alpha=0.5, line_width=1)
    
    #Couleur des liens etc
    network_graph.edge_renderer.selection_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
    network_graph.edge_renderer.hover_glyph = MultiLine(line_color=edge_highlight_color, line_width=2)
    
    #Ca c'est pour la subrillance des liens et des noeuds
    network_graph.selection_policy = NodesAndLinkedEdges()
    network_graph.inspection_policy = NodesAndLinkedEdges()
    
    
    #Ici on définit les couleurs et on les appliquent 
    minimum_value_color = min(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    maximum_value_color = max(network_graph.node_renderer.data_source.data[color_by_this_attribute])
    network_graph.node_renderer.glyph = Circle(size=size_by_this_attribute, fill_color=linear_cmap(color_by_this_attribute, color_palette, minimum_value_color, maximum_value_color))
    
    ############################################################################################################################################################
    
    #On fais le rendu final
    plot.renderers.append(network_graph)
    #Affichage
    show(plot)
    #Enregistrement dans le répertoire courant
    save(plot,filename=str(titre)+".html")

