import pandas as pd

from utilities import logerr


class MovieManager:
    def __init__(self):
        self.NO_MATRIX = False
        try:
            self.recommendation_matrix = pd.read_csv('movie/secret_recommendation_matrix.csv', index_col='movie')
        except OSError:
            self.NO_MATRIX = True
            logerr('No movie/secret_recommendation_matrix.csv')

        self.user_dict = {'Андрей': 0,
                          'Влад': 1,
                          'Артем': 2,
                          'Леха': 3,
                          'Иван': 4,
                          'Димас': 5,
                          'Санек': 6}

    def recommend(self, name: str):
        if self.NO_MATRIX is True:
            return 'Sorry, this command does not work yet'
        if name not in self.user_dict.keys():
            return 'ТЫ ДАЖЕ НЕ ГРАЖДАНИН! Введите имя гражданина SMOrc'
        user_id = str(self.user_dict[name])
        sort_matrix = self.recommendation_matrix.sort_values(by=user_id, ascending=False).head(10)
        return '\n'.join([sort_matrix.index[i] for i in range(10)])

    def get_today_films(self):
        pass
