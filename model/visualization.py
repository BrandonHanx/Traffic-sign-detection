from keras.models import load_model
from keras.utils import plot_model

model=load_model('traffic_sign.model')
plot_model(model, to_file='model.png', show_shapes=True)