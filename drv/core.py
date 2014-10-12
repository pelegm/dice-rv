"""
.. core.py

Discrete random variables - core module.
"""

import pspace


class DRV(object):
    """ A general Discrete Random Variable. Treated as categorical. May have
    finite or infinite support.

    A discrete random variable is simply a probability space equipped with a
    function from that probability space into some outcome set, which is
    usually, but not always, the set of reals.

    A DRV comes with a *name*, which identifies the variable. """
    def __init__(self, pspace, func, name):
        self.pspace = pspace
        self.func = func
        self.name = name

    ## ----- Representation ----- ##

    @property
    def _cls(self):
        """ The class name. """
        return self.__class__.__name__

    def __repr__(self):
        return "{self._cls}({self.name})".format(self=self)

    def __str__(self):
        return self.name

    ## ----- Probability Properties ----- ##

    def mode(self):
        """ The value at which the probability mass function takes its maximum
        value.

        .. warning:: the mode is not necessarily unique. If more than one mode
        exists, this is an arbitrary mode. """
        raise NotImplementedError

    def support(self):
        """ The values at which the probability mass function is positive. """
        raise NotImplementedError

    ## ----- Probability Methods ----- ##

    def pmf(self, k):
        """ Return the probability mass function at *k*. """
        raise NotImplementedError

    ## ----- Operations ----- ##

    def flatten(self):
        """ Return a random variable with a new probability space whose sample
        set is the inverse image of func. """
        raise NotImplementedError

    def map(self, function, name, klass=None, flatten=False):
        """ Return a random variable whose values are the application of
        *function* to self's values. """
        klass = klass or self.__class__
        func = lambda x: function(self.func(x))
        drv = klass(self.pspace, func, name)
        if not flatten:
            return drv
        return drv.flatten()


class FDRV(object):
    """ A finite (general) Discrete Random Variable. Treated as categorical.

    *name* is an identifier for the random variable. *xs* are the possible
    values (categories), and *ps* are the distributions. *xs* and *ps* are
    checked for correctedness, and *ps* are normalized. """
    def __init__(self, name, xs, ps):
        self.pspace = pspace.FDPSpace(ps)
        self.xs = xs
        self._xdict = dict(enumerate(xs))
        self.name = name

    def func(self, k):
        return self._xdict[k]

    @property
    def items(self):
        return zip(self.xs, self.pspace.ps)

    @property
    def mode(self):
        """ The value at which the probability mass function takes its maximum
        value.

        .. warning:: the mode is not necessarily unique. If more than one mode
        exists, this is an arbitrary mode. """
        return max(self.items, key=lambda t: t[1])[0]

    @property
    def support(self):
        """ The values at which the probability mass function is positive. """
        return [x for x, p in self.items if p > 0]

    ## ----- Probability Methods ----- ##

    def _cdf(self, i):
        """ Return the cumulative distribution function at the category whose
        index is *i*. """
        return sum(p for j, (x, p) in enumerate(self.items) if j <= i)

    def cdf(self, k):
        """ Return the cumulative distribution function at *k*. """
        try:
            return self._cdf(self.xs.index(k))
        except ValueError:
            raise ValueError("Category '{}' is not supported.".format(k))

    def pmf(self, k):
        """ Return the probability mass function at *k*. """
        try:
            i = self.xs.index(k)
        except ValueError:
            return 0.
        return self.pspace.ps[i]

    ## ----- Probability Inverse Methods ----- ##

    def ppf(self, q):
        """ Return the percent point function (inverse CDF) at *q* Formally,
        this is the infimum over all x's in the real line for which *q* is at
        most the CDF of x. """
        if not 0 < q <= 1:
            raise ValueError(PPF_DOMAIN)

        ## TODO: This is extremely inefficient (o(n^2)) when the set of xs is
        ## large; we should probably consider using bisect here, to make it
        ## o(nlog(n))
        for x in self.xs:
            if self.cdf(x) >= q:
                return x

        ## Just to make sure some value is returned; may be bugged in case of
        ## rounding errors
        return self.xs[-1]

    ## ----- Probability Log Methods ----- ##

    def logpmf(self, k):
        """ Return the log of the probability mass function at *k*. """
        return np.log(self.pmf(k))

    ## ----- Operations ----- ##

    def binop(self, other, operator, name, klass=None):
        """ return a new discrete random variable, which is the result of
        *operator* on *self* and *other*. """
        ## 'other' is not a random variable, we don't know how to handle that
        if not isinstance(other, DRV):
            return NotImplemented

        ## We may need to be able to handle it
        raise NotImplementedError
