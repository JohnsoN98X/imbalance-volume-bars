import pandas as pd
import numpy as np 

class ImbalanceVolumeBars:
    """
    Constructs volume imbalance bars from OHLCV financial time series data.
    Bars are formed when the absolute value of the cumulative volume imbalance
    exceeds an adaptive threshold based on an exponential moving average.

    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe containing at least the following columns:
        ['open', 'high', 'low', 'close', 'volume']
    """

    def __init__(self, df):
        """
        Initialize the ImbalanceVolumeBars object with a copy of the input dataframe.
        """
        self.df = df.copy()
        self.results = {}

    def make_bars(self, alpha):
        """
        Generate imbalance volume bars using a probabilistic threshold mechanism.

        Parameters:
        -----------
        alpha : float
            Smoothing parameter for the exponentially weighted threshold.
            Must be between 0 and 1. A lower alpha yields smoother thresholds.

        Returns:
        --------
        pandas.DataFrame
            A DataFrame indexed by 'Datetime', with one row per completed bar,
            containing aggregated OHLCV data and total barCount.
        """
        diffs = self.df['close'].diff().to_numpy()[1:]
        beta = np.where(diffs > 0, 1, -1)
        df_ = self.df.iloc[1:]

        # Extract columns as NumPy arrays for speed
        volume_arr = df_['volume'].to_numpy()
        open_arr = df_['open'].to_numpy()
        high_arr = df_['high'].to_numpy()
        low_arr = df_['low'].to_numpy()
        close_arr = df_['close'].to_numpy()
        date_arr = df_.index.to_numpy()

        # Initialize state
        cumulative_theta = 0
        threshold = 1
        start_index = 0

        # Containers for diagnostics and bar storage
        theta_list = []
        cumulative_theta_list = []
        threshold_list = []
        bar_list = []

        for i, bt in enumerate(beta):
            volume = volume_arr[i]
            theta = volume * bt
            cumulative_theta += theta
            threshold = alpha * abs(theta) + (1 - alpha) * threshold

            theta_list.append(theta)
            cumulative_theta_list.append(cumulative_theta)
            threshold_list.append(threshold)

            if abs(cumulative_theta) > threshold:
                sl = slice(start_index, i + 1)
                bar_dict = {
                    'Open': open_arr[sl][0],
                    'High': high_arr[sl].max(),
                    'Low': low_arr[sl].min(),
                    'Close': close_arr[sl][-1],
                    'Volume': volume_arr[sl].sum(),
                    'Datetime': date_arr[i]
                }
                bar_list.append(bar_dict)
                cumulative_theta = 0
                start_index = i + 1

        bars_df = pd.DataFrame(bar_list).set_index('Datetime')

        # Store internal diagnostic attributes
        self._beta = beta
        self._theta_list = theta_list
        self._cumulative_theta_list = cumulative_theta_list
        self._threshold_list = threshold_list

        return bars_df

    @property
    def beta(self):
        """
        Return the directional indicator array: +1 for upward movement, -1 for downward.
        """
        return np.array(self._beta)

    @property
    def imbalance(self):
        """
        Return the list of θ_t = volume × β_t at each time step.
        """
        return np.array(self._theta_list)

    @property
    def cumulative_imbalance(self):
        """
        Return the cumulative sum of imbalance values (θ).
        
        ⚠ Note: This is the *raw* cumulative value, which can be positive or negative.
        However, bar formation logic relies on the *absolute* value of the cumulative imbalance
        exceeding the dynamic threshold.
        """
        return np.array(self._cumulative_theta_list)

    @property
    def thresholds(self):
        """
        Return the list of dynamic thresholds at each time step.
        """
        return np.array(self._threshold_list)
