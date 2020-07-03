import numpy as np
import pandas as pd
import sys
from sklearn import datasets
from sklearn.cluster import SpectralClustering 
from sklearn.preprocessing import MinMaxScaler

def PCAAlgo(data,k):

    #Finding meanvalue for centroid
    MeanValue = np.mean(x_data, axis =0)
    Diff = x_data - MeanValue
    # Covariance Matrix
    Covar=np.cov(Diff.T)
    EigenVals, EigenVecs = np.linalg.eig(Covar)
    i = np.argsort(EigenVals)[::-1]
    EigenVecs = EigenVecs[:,i]

    EigVecK = EigenVecs[:,:k]
    ReducedData = np.dot(Diff, EigVecK)

    return ReducedData



def SpectralCluster(x_data,y_df):
    mms = MinMaxScaler()
    mms.fit(x_data)
    Xnorm = mms.transform(x_data)
    sc = SpectralClustering(n_clusters = 3)
    sc.fit(Xnorm)
    labels = y_data
    unique_labels = np.unique(labels)
    n_clusters_ = len(unique_labels)

    Clustered = Xnorm.copy()
    Clustered = pd.DataFrame(Clustered)

    Clustered.loc[:,'NewCluster'] = sc.labels_ # append labels to points
    #Clustered.sample(5)

    frames = [y_df['Cluster'], Clustered['NewCluster']]
    result = pd.concat(frames, axis = 1)

    for ClusterNum in range(3):

        OneCluster = pd.DataFrame(result[result['NewCluster'] == ClusterNum].groupby('Cluster').size())
        OneCluster.columns=['Size']
        
        NewDigit = OneCluster.index[OneCluster['Size'] == OneCluster['Size'].max()].tolist()


        rowIndex = result.index[result['NewCluster'] == ClusterNum]
        result.loc[rowIndex, 'Label'] = NewDigit[0]
        
    
    # print('Spectral clustering Accuracy')
    

    Correct = (y_df['Cluster'] == result['Label']).sum()
    Accuracy = round(Correct/y_df.shape[0],3)
    print('Accuracy ', Accuracy)

    return Accuracy



if __name__ == "__main__":
    data = pd.read_csv(sys.argv[1],sep = '\t', header = None).values
    x_data = np.array([data[i][0].split(',')[:-1] for i in range(len(data))])
    x_data = x_data.astype(np.float)
    y_data = np.array([data[i][0].split(',')[-1] for i in range(len(data))])
    y_data = np.where(y_data == 'Iris-setosa', 0, y_data)
    y_data = np.where(y_data == 'Iris-versicolor', 1, y_data)
    y_data = np.where(y_data == 'Iris-virginica', 2, y_data)
    y_df = pd.DataFrame(columns = ['Cluster'], data = y_data)

    k = 2

    ReducedData = PCAAlgo(x_data,k)

    ##Spectral Clustering with Original data
    print('Spectral Clustering accuracy with Original data')
    SpectralCluster(x_data,y_df)

    print('Spectral Clustering accuracy with reduced dimensional data')
    SpectralCluster(ReducedData,y_df)



