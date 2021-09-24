class HeatWaveIndex:
    """
    A class used to represent a heat wave index.
    
    Attributes
    ----------
    name : str
        The name of the index. For predefined indices it follows the naming
        conventions of Perkins & Alexander (2013)
    var : str, one of "tmin" or "tmax"
        The meteorological variable.
    pct : int
        The percentile used as a threshold.
    fixed_thres : int or float
        The absolute threshold of the meteorological value. If both pct and
        fixed_thres are set, pct has precedence over fixed_thres.
    min_duration : int
        The minimum number of consecutive days should last so that a warm event
        is considered a heat wave. 
    window_length : int
        The total number of days that a moving window has when computing the
        percentile value for each day.
    """

    def __init__(
        self, name, var, pct, fixed_thres, min_duration, window_length
    ):
        self.name = name
        self.var = var
        self.pct = pct
        self.fixed_thres = fixed_thres
        self.min_duration = min_duration
        self.window_length = window_length


def index(
    name=None,
    var=None,
    pct=None,
    fixed_thres=None,
    min_duration=None,
    window_length=None,
):
    """
    Create a predefined or custom HeatWaveIndex object.

    Parameters
    ----------
    name : str
        The name of the index. For predefined indices it follows the naming
        conventions of Perkins & Alexander (2013)
    var : str
        The meteorological variable.
    pct : int
        The percentile used as a threshold.
    fixed_thres : int or float
        The absolute threshold of the meteorological value. If both pct and
        fixed_thres are set, pct has precedence over fixed_thres.
    min_duration : int
        The minimum number of consecutive days should last so that a warm event
        is considered a heat wave. 
    window_length : int
        The total number of days that a moving window has when computing the
        percentile value for each day.
    
    Returns
    -------
    HeatWaveIndex object
    """
    if name == "ctn90pct":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmin",
            pct=90,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif name == "ctn95pct":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmin",
            pct=95,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif name == "ctx90pct":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif name == "ctx95pct":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=95,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif name == "hot_days":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=None,
            fixed_thres=35,
            min_duration=1,
            window_length=1,
        )
    elif name == "hot_events_daytime":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=None,
            fixed_thres=35,
            min_duration=3,
            window_length=1,
        )
    elif name == "hot_events_nighttime":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmin",
            pct=None,
            fixed_thres=20,
            min_duration=3,
            window_length=1,
        )
    elif name == "summer_days":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=None,
            fixed_thres=25,
            min_duration=1,
            window_length=1,
        )
    elif name == "tn90p":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmin",
            pct=90,
            fixed_thres=None,
            min_duration=1,
            window_length=5,
        )
    elif name == "tropical_nights":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmin",
            pct=None,
            fixed_thres=20,
            min_duration=1,
            window_length=1,
        )
    elif name == "tx90p":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=1,
            window_length=5,
        )
    elif name == "wsdi":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=6,
            window_length=5,
        )
    elif name == "test_index":
        hw_index = HeatWaveIndex(
            name=name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=3,
            window_length=3,
        )
    else:
        hw_index = HeatWaveIndex(
            name=name,
            var=var,
            pct=pct,
            fixed_thres=fixed_thres,
            min_duration=min_duration,
            window_length=window_length,
        )

    if hw_index.name is None:
        hw_index.name = "custom"

    if hw_index.window_length is None:
        hw_index.window_length = 1

    return hw_index
