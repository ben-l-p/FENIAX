import jax.numpy as jnp
import jax
from functools import partial
from fem4inas.intrinsic.functions import H0, H1

def compute_velocities(phi1l: jnp.ndarray, q1: jnp.ndarray) -> jnp.ndarray:

    X1 = jnp.tensordot(phi1l, q1, axes=(0,0))  # 6xNnxNt
    return X1

def compute_internalforces(phi2l: jnp.ndarray, q2: jnp.ndarray) -> jnp.ndarray:

    X2 = jnp.tensordot(phi2l, q2, axes=(0,0))  # 6xNnxNt
    return X2

def compute_strains(cphi2l: jnp.ndarray, q2: jnp.ndarray) -> jnp.ndarray:

    X3 = jnp.tensordot(cphi2l, q2, axes=(0,0))  # 6xNnxNt
    return X3

def velocity_Rab():
    ...

def strains_Rab():
    ...
    
def velocity_ra():
    ...

def strains_ra():
    ...

def integrate_X3(carry, x):

    import pdb; pdb.set_trace()
    Cab0_x = x[:, :3]
    kappa = x[:, 3]
    strain = x[:, 4]
    ds = x[0, 5]
    Cab_carry = carry[:, :3]
    Cab0_carry = carry[:, 3:6]
    ra0 = carry[:, 6]
    Ipsi = kappa * ds
    Itheta = jnp.linalg.norm(Ipsi)
    Cab = Cab0_x @ Cab0_carry.T @ Cab_carry @ H0(Itheta, Ipsi)
    ra = ra0 + Cab_carry @ (H1(Itheta, Ipsi, ds) @ (strain + jnp.array([1, 0, 0])))
    y = jnp.hstack([Cab, ra.reshape((3, 1))])
    carry = jnp.hstack([Cab, Cab0_x, ra.reshape((3, 1))])
    return carry, y

def integrate_strains(ra_0n, Cab_0n, X3t, sol, fem):

    integrate_X3
    ds = sol.data.modes.X_xdelta
    C0ab = sol.data.modes.C0ab  # 3x3xNn
    # TODO: make as fori loop
    Cab = jnp.zeros((3, 3, fem.num_nodes))
    ra = jnp.zeros((3, fem.num_nodes))

    comp_nodes = jnp.array(fem.component_nodes[fem.component_names[0]])
    numcomp_nodes = len(comp_nodes)
    Cab0_init = C0ab[:, :, 0]
    init = jnp.hstack([Cab_0n,
                       Cab0_init,
                       ra_0n.reshape((3, 1))])
    ds_i = ds[comp_nodes]
    ds_i = jnp.broadcast_to(ds_i, (3, ds_i.shape[0])).T.reshape((numcomp_nodes, 3, 1))
    strains_i = X3t[:3, comp_nodes].T.reshape((numcomp_nodes, 3, 1))
    kappas_i = X3t[3:, comp_nodes].T.reshape((numcomp_nodes, 3, 1))
    #import pdb; pdb.set_trace()
    C0ab_i = C0ab[:, :, comp_nodes].transpose((2, 0, 1))
    xs = jnp.concatenate([C0ab_i, strains_i, kappas_i,  ds_i], axis=2)
    last_carry, Cra = jax.lax.scan(integrate_X3, init, xs)
    ra = ra.at[:, comp_nodes].set(Cra[:, :, 3].T)
    Cab = Cab.at[:, :, comp_nodes].set(Cra[:, :, :3].transpose((1, 2, 0)))
    
    for ci in fem.component_names[1:]:

        comp_father = fem.component_father
        comp_nodes = jnp.array(fem.component_nodes[ci])
        node_father = fem.component_nodes[comp_father][-1]
        Cab_init = Cab[:, :, node_father]
        Cab0_init = C0ab[:, :, node_father]
        ra_init = ra[:, node_father]
        init = jnp.hstack([Cab_init, Cab0_init,
                           ra_init.reshape((3,1))])
        ds_i = ds[comp_nodes]
        ds_i = jnp.broadcast_to(3, ds_i.shape[0]).T.reshape((numcomp_nodes, 3, 1))
        strains_i = X3t[:3, comp_nodes].T.reshape((numcomp_nodes, 3, 1))
        kappas_i = X3t[3:, comp_nodes].T.reshape((numcomp_nodes, 3, 1))
        C0ab_i = C0ab[:, :, comp_nodes].transponse((1,2,0))
        xs = jnp.concatenate([C0ab_i, strains_i, kappas_i,  ds_i], axis=2)
        last_carry, Cra = jax.lax.scan(integrate_X3, init, xs)
        ra = ra.at[:, comp_nodes].set(Cra[:, :, 3])
        Cab = Cab.at[:, comp_nodes].set(Cra[:, :, :3])
    return Cab, ra
        
        
