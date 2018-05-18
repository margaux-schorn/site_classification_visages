import cv2
import numpy as np
import tensorflow as tf

graph_path = 'site_classification_visages/network/inception_v3_frozen_graph.pb'
labels_path = 'site_classification_visages/network/liste_labels.txt'


def analyser_images(images):
    resultats = {}
    graph = charger_reseau()

    for img in images:
        path = 'site_classification_visages/static/{}'.format(img.url())
        print(path)
        resultats[img.name] = obtenir_predictions(path, graph)

    print(resultats)

    return resultats


def charger_reseau():
    with tf.Graph().as_default() as graph:
        # Unpersists graph from file
        with tf.gfile.FastGFile(graph_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        return graph


def obtenir_predictions(image_path, graph):
    # Read in the image_data
    resultats = []
    image = cv2.imread(image_path)
    image_data = np.array(image, dtype=np.uint8)
    image_data = image_data.astype('float32')
    image_data = np.multiply(image_data, 1.0 / 255.0)

    image_data = np.resize(image_data, (32, 299, 299, 3))

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile(labels_path)]

    # Feed the image_data as input to the graph and get first prediction
    with tf.Session(graph=graph) as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('InceptionV3/Predictions/Reshape_1:0')
        predictions = sess.run(softmax_tensor,{'input:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            score = "{:2.2f} %".format(score*100)
            resultats.append((human_string, score))
            print('%s (score = %s)' % (human_string, score))

    return resultats
