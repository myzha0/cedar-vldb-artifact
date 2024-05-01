import tensorflow as tf
import fastflow as ff
import librosa
import random
import numpy as np

from eval_app_runner import App

DATASET_LOC="/home/myzhao/ember/evaluation/datasets/cv/*"
SAMPLE_FREQ = 8000
N_FFT = 400
FREQ_MASK_PARAM = 80
TIME_MASK_PARAM = 80
N_MELS = 256

def time_mask(x):
    t = np.random.uniform(low=0.0, high=TIME_MASK_PARAM)
    t = int(t)
    tau = x.shape[1]
    t0 = random.randint(0, tau - t)
    x[:, t0 : t0 + t] = 0
    return x


def frequency_mask(x):
    f = np.random.uniform(low=0.0, high=FREQ_MASK_PARAM)
    f = int(f)
    v = x.shape[0]
    f0 = random.randint(0, v - f)
    x[f0 : f0 + f, :] = 0
    return x


def mel(x):
    return librosa.feature.melspectrogram(
        S=x, sr=SAMPLE_FREQ, n_mels=N_MELS, n_fft=N_FFT
    )

def _process_path(path):
    x, sr = librosa.load(path.numpy())
    x = librosa.resample(y=x, orig_sr=sr, target_sr=SAMPLE_FREQ)
    x = np.abs(librosa.stft(x, n_fft=N_FFT)) ** 2
    x = librosa.effects.time_stretch(x, rate=0.8, n_fft=N_FFT)
    x = time_mask(x)
    x = frequency_mask(x)
    x = mel(x)
    return x

def process_path(x):
    res = tf.py_function(_process_path, [x], [tf.float32])
    return (res, tf.constant(0.0))

class CVModel(ff.FastFlowModel):
# class CVModel(tf.keras.Model):
    def __init__(self):
        super().__init__()

    def call(self, inputs):
        # do nothing
        return inputs

    def __deepcopy__(self):
        return CVModel()
    
class CVApp(App):
# class CVApp():
    def __init__(self, args, config):
        super().__init__(args, config)
        # pass

    def dummy_loss(self, y_true, y_pred):
        return tf.constant(0.0)

    def create_model(self):
        model = CVModel()

        model.compile(optimizer="adam", loss=self.dummy_loss)
        return model

    def create_dataset(self, num_parallel):
        ds = tf.data.Dataset.list_files(DATASET_LOC, shuffle=False)
        ds = ds.map(
            process_path, num_parallel_calls=num_parallel, name="prep_begin"
        )
        ds = ds.batch(1)
        ds = ds.prefetch(buffer_size=tf.data.AUTOTUNE)
        return ds

    def create_valid_dataset(self, num_parallel):
        return None

if __name__ == "__main__":
    app = CVApp(None, None)
    ds = app.create_dataset(1)

    # for x in ds:
    #     print(x)
    #     break
    model = app.create_model()

    # config = ff.FastFlowConfig.from_yaml("/home/myzhao/FastFlow/examples/config.yaml")

    model.fit(ds, epochs=10)

