class HeatwaveIndex:
    def __init__(
        self, name, var, pct, fixed_thres, min_duration, window_length
    ):
        self.name = name
        self.var = var
        self.pct = pct
        self.fixed_thres = fixed_thres
        self.min_duration = min_duration
        self.window_length = window_length


def _load_index(index_name):
    if index_name == "ctx95pct":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmax",
            pct=95,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif index_name == "ctn95pct":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmin",
            pct=95,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif index_name == "ctx90pct":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif index_name == "ctn90pct":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmin",
            pct=90,
            fixed_thres=None,
            min_duration=3,
            window_length=15,
        )
    elif index_name == "tx90p":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=1,
            window_length=5,
        )
    elif index_name == "tn90p":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmin",
            pct=90,
            fixed_thres=None,
            min_duration=1,
            window_length=5,
        )
    elif index_name == "wsdi":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=6,
            window_length=5,
        )
    elif index_name == "test":
        hw_index = HeatwaveIndex(
            name=index_name,
            var="tmax",
            pct=90,
            fixed_thres=None,
            min_duration=3,
            window_length=3,
        )
    return hw_index
