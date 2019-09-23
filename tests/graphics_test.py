import pyglet
import graphics
import grid

"""
quick tests to make sure drawing functions are correct (this should be deleted once fully tested)
"""

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540

window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

test_batch = pyglet.graphics.Batch()

# [ Grid() ]
grid_tests = [  grid.Grid(  [ 50, 400 ],
                            125,
                            100,
                            5,
                            5,
                            labelColor = (255, 0, 0, 150),
                            alpha = True,
                            thickness = 2.0 ),

                grid.Grid(  [ 750, 50 ],    # TODO: need to update Grid so it resizes with the window
                            150,
                            300,
                            6,
                            9,
                            color = (195, 200, 15),
                            thickness = 5.0,
                            label = True,
                            alpha = True,
                            labelColor = (0, 0, 255, 255)   ),

                grid.Grid(  [ 350, 350 ],
                            275,
                            150,
                            4,
                            7,
                            color = (150, 75, 250),
                            labelColor = (255, 0, 0, 150),
                            alpha = True,
                            label = True,
                            thickness = 10.5 )   ]

# [ vertex_list, drawing_mode ]
graphics_tests = [ [        graphics.generateCircle(    [ 100, 300 ],
                                                        75,
                                                        20,
                                                        fill = False    ),
                            pyglet.gl.GL_LINE_STRIP     ],

                    [       graphics.generateCircle(    [ 300, 200],
                                                        150,
                                                        10,
                                                        color = (235, 140, 50),
                                                        fill = True ),
                            pyglet.gl.GL_TRIANGLES      ],

                    [       graphics.generateCircle(    [ 50, 50 ],
                                                        50,
                                                        50,
                                                        fill = True ),
                            pyglet.gl.GL_TRIANGLES      ],

                    [       graphics.generateCircle(    [ 600, 150 ],
                                                        100,
                                                        15,
                                                        color = (100, 100, 100) ),
                            pyglet.gl.GL_LINE_STRIP     ],
                ]

@window.event
def on_draw():
    for grid in grid_tests:
        grid.draw()

    for graphics, mode in graphics_tests:
        graphics.draw(mode)

pyglet.app.run()
