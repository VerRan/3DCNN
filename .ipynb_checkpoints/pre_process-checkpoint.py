import videoto3d
from os import *
# import tqdm

class Pre_process:
        
    def __init__(self, width):
        self.width = width
        
    def loaddata(video_dir, vid3d, nclass, result_dir, color=False, skip=True):
        files = os.listdir(video_dir)
        X = []
        labels = []
        labellist = []

#         pbar = tqdm(total=len(files))

        for filename in files:
#             pbar.update(1)
            if filename == '.DS_Store':
                continue
            name = os.path.join(video_dir, filename)
            label = vid3d.get_UCF_classname(filename)
            if label not in labellist:
                if len(labellist) >= nclass:
                    continue
                labellist.append(label)
            labels.append(label)
            X.append(vid3d.video3d(name, color=color, skip=skip))

#         pbar.close()
        with open(os.path.join(result_dir, 'classes.txt'), 'w') as fp:
            for i in range(len(labellist)):
                fp.write('{}\n'.format(labellist[i]))

        for num, label in enumerate(labellist):
            for i in range(len(labels)):
                if label == labels[i]:
                    labels[i] = num
        if color:
            return np.array(X).transpose((0, 2, 3, 4, 1)), labels
        else:
            return np.array(X).transpose((0, 2, 3, 1)), labels

        
    def process():
        nclass = 8
        depth = 15
        skip = False
        color = True
        img_rows, img_cols, frames = 32, 32, depth

        channel = 3 if color else 1
        fname_npz = 'dataset_{}_{}_{}.npz'.format(
                nclass, depth, skip)
        output = 'default-output/'
        videos = 'dataset/'

        vid3d = videoto3d.Videoto3D(img_rows, img_cols, frames)
        nb_classes = nclass
        if os.path.exists(fname_npz):
                loadeddata = np.load(fname_npz)
                X, Y = loadeddata["X"], loadeddata["Y"]
        else:
                x, y = loaddata(videos, vid3d, nclass,
                                output, color, skip)
                X = x.reshape((x.shape[0], img_rows, img_cols, frames, channel))
                Y = np_utils.to_categorical(y, nb_classes)

                X = X.astype('float32')
                np.savez(fname_npz, X=X, Y=Y)
        print('Saved dataset to dataset.npz.')
        print('X_shape:{}\nY_shape:{}'.format(X.shape, Y.shape))


# def main():
#     process()
#     nclass = 8
#     depth = 15
#     skip = False
#     color = True
#     img_rows, img_cols, frames = 32, 32, depth

#     channel = 3 if color else 1
#     fname_npz = 'dataset_{}_{}_{}.npz'.format(
#             nclass, depth, skip)
#     output = 'default-output/'
#     videos = 'dataset/'

#     vid3d = videoto3d.Videoto3D(img_rows, img_cols, frames)
#     nb_classes = nclass
#     if os.path.exists(fname_npz):
#             loadeddata = np.load(fname_npz)
#             X, Y = videoto3d.loadeddata["X"], loadeddata["Y"]
#     else:
#             x, y = videoto3d.loaddata(videos, vid3d, nclass,
#                             output, color, skip)
#             X = x.reshape((x.shape[0], img_rows, img_cols, frames, channel))
#             Y = np_utils.to_categorical(y, nb_classes)

#             X = X.astype('float32')
#             np.savez(fname_npz, X=X, Y=Y)
#     print('Saved dataset to dataset.npz.')
#     print('X_shape:{}\nY_shape:{}'.format(X.shape, Y.shape))