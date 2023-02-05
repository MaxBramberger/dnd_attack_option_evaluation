import numpy as np


class Die:
    def __init__(self, faces:int = 20, cache_size: int =1000)->None:
        self._faces=faces
        self._cache_size=cache_size
        self._cached_rolls=np.empty(shape=(0,),dtype=int)

    def roll(self) -> int:
        if len(self._cached_rolls)==0:
            self._cached_rolls=np.random.choice(np.arange(self._faces)+1,self._cache_size)
        result=self._cached_rolls[-1]
        self._cached_rolls=self._cached_rolls[:-1]
        return result



