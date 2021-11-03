# Mapping of camera filter name: reference catalog filter name; each reference filter must exist in the refcat. 
# Note that this does not perform any bandpass corrections: it is just a lookup.
for source, target in [
        ('N419', 'g'),
        ('N540', 'g'),
        ('N708', 'i'),
        ('N964', 'z'),
    ]:
    config.filterMap[source] = target
