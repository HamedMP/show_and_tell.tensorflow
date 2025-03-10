#-*- coding: utf-8 -*-
"""
Optimizers for multimodal ranking
"""
import theano
import theano.tensor as tensor
import numpy
import ipdb

# name(hyperp, tparams, grads, inputs (list), cost) = f_grad_shared, f_update
def adam(lr, params, grads, inp, cost):
    gshared = [theano.shared(p.get_value() * 0.) for p in params]
    gsup = [(gs, g) for gs, g in zip(gshared, grads)]

    f_grad_shared = theano.function(inp, cost, updates=gsup, profile=False, allow_input_downcast=True)
    # f_grad_shared 는 이번 grad 값들을 저장

    lr0 = lr#0.0002
    b1 = 0.1
    b2 = 0.001
    e = 1e-8

    updates = []

    i = theano.shared(numpy.float32(0.))
    i_t = i + 1.
    fix1 = 1. - b1**(i_t)
    fix2 = 1. - b2**(i_t)
    lr_t = lr0 * (tensor.sqrt(fix2) / fix1)

    for p, g in zip(params, gshared):
        m = theano.shared(p.get_value() * 0.)
        v = theano.shared(p.get_value() * 0.)
        m_t = (b1 * g) + ((1. - b1) * m)
        v_t = (b2 * tensor.sqr(g)) + ((1. - b2) * v)
        g_t = m_t / (tensor.sqrt(v_t) + e)
        p_t = p - (lr_t * g_t)
        updates.append((m, m_t))
        updates.append((v, v_t))
        updates.append((p, p_t))
    updates.append((i, i_t))

    f_update = theano.function([lr], [], updates=updates, on_unused_input='ignore', profile=False, allow_input_downcast=True)

    return f_grad_shared, f_update
