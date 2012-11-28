from pysketcher import *

u = SketchyFunc2('$u(t)$', name_pos='end')
n = 7
t_mesh = [i*2.25/(n-1) for i in range(n)]

u = SketchyFunc2('$u(t)$', name_pos='end')
t_mesh = [0, 2, 4, 6, 8]

u = SketchyFunc3()
t_mesh = linspace(0, 6, 8)  # bra
t_mesh = linspace(0, 6, 6)


t_min1 = t_mesh[0] - 0.1*(t_mesh[-1] - t_mesh[0])
t_max1 = t_mesh[-1] + 0.2*(t_mesh[-1] - t_mesh[0])
t_min2 = t_mesh[0] - 0.2*(t_mesh[-1] - t_mesh[0])
t_max2 = t_mesh[-1] + 0.3*(t_mesh[-1] - t_mesh[0])
u_max = 1.3*max([u(t) for t in t_mesh])
u_min = -0.2*u_max

drawing_tool.set_coordinate_system(t_min2, t_max2, u_min, u_max, axis=False)
drawing_tool.set_linecolor('black')

r = 0.005*(t_max2-t_min2)     # radius of circles placed at mesh points
discrete_u = Composition({i: Composition(dict(
    circle=Circle(point(t, u(t)), r).set_filled_curves('black'),
    u_point=Text('$u_%d$' % i,
                 point(t, u(t)) + (point(0,5*r)
                                   if i > 0 else point(-5*r,0))),
    )) for i, t in enumerate(t_mesh)})

interpolant = Composition({
    i: Line(point(t_mesh[i-1], u(t_mesh[i-1])),
            point(t_mesh[i], u(t_mesh[i]))).set_linewidth(1)
    for i in range(1, len(t_mesh))})

axes = Composition(dict(x=Axis(point(0,0), t_max1, '$t$',
                               label_spacing=(1/45.,-1/30.)),
                        y=Axis(point(0,0), 0.8*u_max, '$u$',
                               rotation_angle=90)))
h = 0.03*u_max  # tickmarks height
nodes = Composition({i: Composition(dict(
    node=Line(point(t,h), point(t,-h)),
    name=Text('$t_%d$' % i, point(t,-3.5*h))))
                     for i, t in enumerate(t_mesh)})
illustration = Composition(dict(u=discrete_u,
                                mesh=nodes,
                                axes=axes)).set_name('fdm_u')
drawing_tool.erase()
illustration.draw()
drawing_tool.display()
drawing_tool.savefig(illustration.get_name())

exact = u.set_linestyle('dashed').set_linewidth(1)
exact.draw()
drawing_tool.display()
drawing_tool.savefig('%s_ue' % illustration.get_name())

interpolant.draw()
drawing_tool.display()
drawing_tool.savefig('%s_uei' % illustration.get_name())

raw_input()
