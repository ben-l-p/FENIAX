import jax.numpy as jnp
import numpy as np
import jax
import fem4inas.intrinsic.xloads as xloads
import fem4inas.intrinsic.postprocess as postprocess
import fem4inas.intrinsic.dq_common as common
import fem4inas.intrinsic.functions as functions
from functools import partial
#@jax.jit
def dq_20g1(t, q, *args):
    """Clamped Structural dynamics, free vibrations."""

    gamma1, gamma2, omega, states = args[0]
    q1 = q[states['q1']]
    q2 = q[states['q2']]
    F1, F2 = common.f_12(omega, gamma1, gamma2, q1, q2)
    F = jnp.hstack([F1, F2])
    return F

#@jax.jit
def dq_20g11(t, q, *args):
    """Structural dynamic follower point forces."""
    
    (gamma1, gamma2, omega, phi1, x,
     force_follower, states) = args[0]

    q1 = q[states['q1']]
    q2 = q[states['q2']]
    eta = xloads.eta_pointfollower(t,
                                   phi1,
                                   x,
                                   force_follower)
    F1, F2 = common.f_12(omega, gamma1, gamma2, q1, q2)
    F1 += eta
    F = jnp.hstack([F1, F2])
    return F

def dq_20g121(t, q, *args):
    """Structural dynamic dead point forces."""
    
    (gamma1, gamma2, omega, phi1l, psi2l,
     x, force_dead,
     states,
     X_xdelta,
     C0ab,
     component_names, num_nodes,
     component_nodes, component_father) = args[0]
    q1i = q[states['q1']]
    q2i = q[states['q2']]
    #@jax.jit
    def _dq_20g121(t, q1, q2):
        X3t = postprocess.compute_strains_t(
            psi2l, q2)
        Rab = postprocess.integrate_strainsCab(
            jnp.eye(3), X3t,
            X_xdelta, C0ab,
            component_names,
            num_nodes,
            component_nodes,
            component_father)
        eta = xloads.eta_pointdead(t,
                                   phi1l,
                                   x,
                                   force_dead,
                                   Rab)
        F1, F2 = common.f_12(omega, gamma1, gamma2, q1, q2)
        F1 += eta
        F = jnp.hstack([F1, F2])
        return F
    F = _dq_20g121(t, q1i, q2i)
    return F

def dq_20g242(t, q, *args):
    """Free Structural dynamic dead point forces."""
    
    (gamma1, gamma2, omega, phi1l, psi2l,
     x, force_dead,
     states,
     X_xdelta,
     C0ab,
     component_names, num_nodes,
     component_nodes, component_father) = args[0]
    q1 = q[states['q1']]
    q2 = q[states['q2']]
    qr = q[states['qr']]
    qr0 = qr[0]
    qrx = qr[1:]
    Rab0 = (2 * jnp.tensordot(qrx, qrx, axes=0) +
            (qr0 ** 2 - jnp.dot(qrx, qrx)) * jnp.eye(3) +
            2 * qr0 * functions.tilde(qrx))
    X3t = postprocess.compute_strains_t(
        psi2l, q2)
    # X1t = postprocess.compute_velocities_t(phi1l, q1)
    X1_0 = jnp.tensordot(phi1l[:,:,0], q1, axes=(0,0)) # local velocity node 0 (6x1)
    Rab_init = C0ab[:, :, 0]
    X1_0g = Rab_init @ X1_0
    X1_0w = X1_0g[3:6]
    Rab = postprocess.integrate_strainsCab(
        Rab0, X3t,
        X_xdelta, C0ab,
        component_names,
        num_nodes,
        component_nodes,
        component_father)
    eta = xloads.eta_pointdead(t,
                               phi1l,
                               x,
                               force_dead,
                               Rab)
    F1, F2 = common.f_12(omega, gamma1, gamma2, q1, q2)
    F1 += eta
    Fr0 = -0.5 * jnp.dot(X1_0w, qrx)
    Frx = 0.5 * (qr0 * X1_0w - functions.tilde(X1_0w) @ qrx)
    Fr = jnp.hstack([Fr0, Frx])
    F = jnp.hstack([F1, F2, Fr])
    return F

#@jax.jit
#@partial(jax.jit, static_argnames=['q'])
def dq_20g21(t, q, *args):
    """Gust response."""
    
    (gamma1, gamma2, omega, states,
     num_modes, num_poles,
     A0hat, A1hat, A2hatinv, A3hat,
     u_inf, c_ref, poles,
     xgust, F1gust, Flgust) = args[0]

    q1 = q[states['q1']]
    q2 = q[states['q2']]
    q0 = -q2 / omega
    ql = q[states['ql']]
    #jax.debug.breakpoint()
    #ql_tensor = ql.reshape((num_modes, num_poles))
    eta_s = xloads.eta_rogerstruct(q0, q1, ql,
                                   A0hat, A1hat,
                                   num_modes, num_poles)
    eta_gust = xloads.eta_rogergust(t, xgust, F1gust)
    #jax.debug.breakpoint()
    F1, F2 = common.f_12(omega, gamma1, gamma2, q1, q2)
    F1 += eta_s + eta_gust
    #jax.debug.print("time: {t}", t=t)
    #jax.debug.print("eta_aero: {eta_aero}", eta_aero=(eta_gust))
    #jax.debug.breakpoint()
    F1 = A2hatinv @ F1 #Nm
    Fl = xloads.lags_rogerstructure(A3hat, q1, ql, u_inf,
                                    c_ref, poles,
                                    num_modes, num_poles)  # NlxNm
    # Fl1 = xloads.lags_rogerstructure1(A3hat, q1, ql, u_inf,
    #                                 c_ref, poles,
    #                                 num_modes, num_poles)  # NlxNm
    # Fl2 = xloads.lags_rogerstructure2(A3hat, q1, ql, u_inf,
    #                                 c_ref, poles,
    #                                 num_modes, num_poles)  # NlxNm
    # Fl = Fl1 + Fl2
    Flgust = xloads.lags_rogergust(t, xgust, Flgust)  # NlxNm
    #jax.debug.breakpoint()
    Fl += Flgust
    #Fl = Fl_tensor.reshape(num_modes * num_poles
    return jnp.hstack([F1, F2, Fl])

def dq_20g21l(t, q, *args):
    """Gust response."""
    
    (omega, states,
     num_modes, num_poles,
     A0hat, A1hat, A2hatinv, A3hat,
     u_inf, c_ref, poles,
     xgust, F1gust, Flgust) = args[0]

    q1 = q[states['q1']]
    q2 = q[states['q2']]
    q0 = -q2 / omega
    ql = q[states['ql']]
    #jax.debug.breakpoint()
    #ql_tensor = ql.reshape((num_modes, num_poles))
    eta_s = xloads.eta_rogerstruct(q0, q1, ql,
                                   A0hat, A1hat,
                                   num_modes, num_poles)
    eta_gust = xloads.eta_rogergust(t, xgust, F1gust)
    #jax.debug.breakpoint()
    F1, F2 = common.f_12l(omega, q1, q2)
    F1 += eta_s + eta_gust
    #jax.debug.print("time: {t}", t=t)
    #jax.debug.print("eta_aero: {eta_aero}", eta_aero=(eta_gust))
    #jax.debug.breakpoint()
    F1 = A2hatinv @ F1 #Nm
    Fl = xloads.lags_rogerstructure(A3hat, q1, ql, u_inf,
                                    c_ref, poles,
                                    num_modes, num_poles)  # NlxNm
    # Fl1 = xloads.lags_rogerstructure1(A3hat, q1, ql, u_inf,
    #                                 c_ref, poles,
    #                                 num_modes, num_poles)  # NlxNm
    # Fl2 = xloads.lags_rogerstructure2(A3hat, q1, ql, u_inf,
    #                                 c_ref, poles,
    #                                 num_modes, num_poles)  # NlxNm
    # Fl = Fl1 + Fl2
    Flgust = xloads.lags_rogergust(t, xgust, Flgust)  # NlxNm
    #jax.debug.breakpoint()
    Fl += Flgust
    #Fl = Fl_tensor.reshape(num_modes * num_poles
    return jnp.hstack([F1, F2, Fl])


@partial(jax.jit, static_argnames=['q'])
def dq_20g273(t, q, *args):
    """Gust response, q0 obtained via integrator q1."""
    
    (gamma1, gamma2, omega, states,
     num_modes, num_poles,
     A0hat, A1hat, A2hatinv, A3hat,
     u_inf, c_ref, poles,
     xgust, F1gust, Flgust) = args[0]

    q1 = q[states['q1']]
    q2 = q[states['q2']]
    ql = q[states['ql']]
    q0 = q[states['q0']]
    #ql_tensor = ql.reshape((num_modes, num_poles))
    eta_s = xloads.eta_rogerstruct(q0, q1, ql,
                                   A0hat, A1hat, A2hatinv,
                                   num_modes, num_poles)
    eta_gust = xloads.eta_rogergust(t, xgust, F1gust)
    F1, F2 = common.f_12(omega, gamma1, gamma2, q1, q2)
    F1 += eta_s + eta_gust
    F1 = A2hatinv @ F1 #Nm
    Fl = xloads.lags_rogerstructure(A3hat, q1, ql, u_inf,
                                    c_ref, poles,
                                    num_modes, num_poles)  # NlxNm
    Flgust = xloads.lags_rogergust(t, xgust, Flgust)  # NlxNm
    Fl += Flgust
    F0 = q1
    #Fl = Fl_tensor.reshape(num_modes * num_poles
    return jnp.hstack([F1, F2, Fl, F0])

#@jax.jit
#@partial(jax.jit, static_argnames=['q'])
# def dq_20g273(t, q, *args):
#     """Gust response, q0 obtained via integrator q1."""
#     (gamma1, gamma2, omega, states,
#      num_modes, num_poles,
#      A0hat, A1hat, A2hatinv, A3hat,
#      u_inf, c_ref, poles,
#      xgust, F1gust, Flgust) = args[0]

#     q1 = q[states['q1']]
#     q2 = q[states['q2']]
#     ql = q[states['ql']]
#     q0 = q[states['q0']]
#     #q0 = -q2 / omega
#     #jax.debug.print("q0: {}", q0)
#     # ql_tensor = ql.reshape((num_modes, num_poles))
#     eta_s = xloads.eta_rogerstruct(q0, q1, ql,
#                                    A0hat, A1hat, A2hatinv,
#                                    num_modes, num_poles)
#     eta_gust = xloads.eta_rogergust(t, xgust, F1gust)
#     F1, F2 = common.f_12(omega, gamma1, gamma2, q1, q2)
#     #F1 += eta_s + eta_gust
#     F1 +=  eta_gust
#     F1 = A2hatinv @ F1 #Nm
#     Fl = xloads.lags_rogerstructure(A3hat, q1, ql, u_inf,
#                                     c_ref, poles,
#                                     num_modes, num_poles)  # NlxNm 
#     Flgust = xloads.lags_rogergust(t, xgust, Flgust)  # NlxNm
#     Fl = Flgust
#     F0 = q1
#     #Fl = Fl_tensor.reshape(num_modes * num_poles
#     return jnp.hstack([F1, F2, Fl, F0])
