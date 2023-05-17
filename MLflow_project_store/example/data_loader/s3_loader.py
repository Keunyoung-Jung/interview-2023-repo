import s3fs
from fastparquet import ParquetFile
import pandas as pd
import random
from time import time

def byte_transform(bytes, to, bsize=1024):
    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize
    return round(r,2)

class DataLoader:
    def __init__(self,
                 chunk_size : int =100000,
                 bucket : str = 'mysterico-feature-store',
                 folder : str = 'mongo34_token.parquet',
                 random_seed : int = int((time() - int(time()))*100000),
                 columns : list = None,
                 depth : int = 2
                 ):
        self.chunk_size = chunk_size
        self.cache = None
        self.dataset = None
        self.counter = 0
        self.num = 0
        self.placeholder = []
        self.bucket = bucket
        self.folder = folder
        self.generator_iterator = self.generator()
        self.select_columns = columns
        
        s3_path = f'{self.bucket}/{self.folder}{"/*"*depth}/*.parquet'
        print(f'Loading parquet list from \"{s3_path}\"...',end='\r')
        s3 = s3fs.S3FileSystem()
        fs = s3fs.core.S3FileSystem()
        
        all_paths_from_s3 = fs.glob(path=s3_path)
        print(f'Loading parquet list from \"{s3_path}\"... complete')
        start_init_time = time()
        print(f'{len(all_paths_from_s3)}files Initialize ...',end='\r')
        myopen = s3.open
        random.Random(random_seed).shuffle(all_paths_from_s3)
        self.fp_obj = ParquetFile(
            all_paths_from_s3,
            open_with=myopen,
            root=f'{self.bucket}/{self.folder}'
            )
        print(f'{len(all_paths_from_s3)}files Initialize ... complete {round(time()-start_init_time,2)}sec')
        self.total_num = self.fp_obj.info['row_groups']
        self.shuffle_seed_list = random.Random(random_seed).sample(range(100000+self.total_num*10),self.total_num)
    def __next__(self):
        return next(self.generator_iterator)
    def __iter__(self) :
        return self.generator_iterator
    @property
    def columns(self) :
        return self.fp_obj.info['columns']
    @property
    def count(self) :
        return self.fp_obj.info['rows']
    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration
    def close(self):
        try:
            self.throw(GeneratorExit)
        except (GeneratorExit, StopIteration):
            pass
        else:
            raise RuntimeError("generator ignored GeneratorExit")
    def generator(self):
        for df in self.fp_obj.iter_row_groups(columns=self.select_columns):
            if self.dataset is None :
                self.dataset = df
            else :
                if len(self.dataset) > self.chunk_size :
                    slicer = len(self.dataset) - self.chunk_size
                    self.dataset = self.dataset.sample(frac=1,random_state=self.shuffle_seed_list[self.num]).reset_index(drop=True)
                    dataset_comp = self.dataset[:-slicer]
                    self.dataset = pd.concat([self.dataset[self.chunk_size:],df])
                    yield dataset_comp
                elif len(self.dataset) < self.chunk_size :
                    self.dataset = pd.concat([self.dataset,df])
                elif len(self.dataset) == self.chunk_size :
                    yield self.dataset
                    self.dataset = df
            self.cache = df
            self.counter += len(df)
            self.num += 1
            print('data loading...',f'{self.num}/{self.total_num}',end='\r')
        self.dataset = self.dataset.sample(frac=1,random_state=self.shuffle_seed_list[self.num-1]).reset_index(drop=True)
        yield self.dataset
        self.dataset = None
        print(self.counter,'data loaded complete!',end='\n')
    

if __name__ == '__main__':
    dl = DataLoader(folder="mongo-sentence-feature2.parquet/uploadedYear=2017",depth=1)
    for df in dl :
        df.to_csv('./data/sentence-feature.csv')
        break
    # dl = DataLoader(folder="mongo-sentence-feature.parquet")
    # print(dl.columns)
    # dl = DataLoader(folder="mongo-sentence-token-feature.parquet")
    # print(dl.columns)
    # dl = DataLoader(folder="mongo-raw-feature.parquet")
    # print(dl.columns)
    # print(dl.count)
    # print(dl.columns)
    # print(len(next(dl)))
    # print(len(next(dl)))
    # print(len(next(dl)))
    # dl2 = DataLoader(random_seed=100)
    # for i in dl2:
    #     print(i.head())
    #     print('\n',len(i))