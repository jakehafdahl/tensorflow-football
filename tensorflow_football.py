import tensorflow as tf
import numpy as np

class TensorFlowModel:
    def __init__(self, x_features_length, y_features_length, lambda_val = .03):
        self.session = tf.Session()
        self.x = tf.placeholder('float', [None, x_features_length], name="X")
        self.y = tf.placeholder('float', [None, y_features_length], name="Y")
        self.theta = tf.Variable(tf.random_normal([x_features_length, y_features_length], stddev=0.01))
        self.lambda_val = tf.constant(lambda_val)
        self.y_predicted = tf.matmul(self.x, self.theta)
        self.regularization_cost_part = tf.cast(tf.mul(self.lambda_val,tf.reduce_sum(tf.pow(self.theta,2))), 'float')
        self.polynomial_cost_part = tf.reduce_sum(tf.pow(self.y_predicted - self.y, 2))

        with tf.name_scope('cost') as scope:
            self.cost_func = tf.add(self.polynomial_cost_part, self.regularization_cost_part);
            cost_summ = tf.scalar_summary("cost", self.cost_func)

        self.training_func = tf.train.GradientDescentOptimizer(0.05).minimize(self.cost_func)

        with tf.name_scope("test") as scope:
            correct_prediction = ((1 - tf.reduce_sum(self.y_predicted - self.y)) * 100)
            self.accuracy = tf.cast(correct_prediction, "float")
            accuracy_summary = tf.scalar_summary("accuracy", self.accuracy)

        self.saver = tf.train.Saver()
        self.merged = tf.merge_all_summaries()
        self.writer = tf.train.SummaryWriter("/tmp/football_logs", self.session.graph_def)
        self.init = tf.initialize_all_variables()

    def set_training_values(self, X, Y, X_test, Y_test):
        self.x_train = X
        self.y_train = Y
        self.x_test = X_test
        self.y_test = Y_test

    def train(self):
        self.session.run(self.init)
        for i in range(0, len(self.x_train) / 10):
            self.session.run(self.training_func, feed_dict={self.x: self.x_train[i*10:i*10+10], self.y: self.y_train[i*10:i*10+10]})
            if i % 10 == 0:
                result = self.session.run([self.merged, self.accuracy], feed_dict={self.x: self.x_test, self.y: self.y_test})
                self.writer.add_summary(result[0], i)
                print "step %d, training accuracy %g"%(i, result[1])

        print "test accuracy %g"%self.accuracy.eval(session=self.session, feed_dict={self.x: self.x_test, self.y: self.y_test})

        save_path = self.saver.save(self.session, "/tmp/football.ckpt")
        print "Model saved in file: ", save_path
        self.session.close()


def normalize_data(matrix):
    averages = np.average(matrix,0)
    mins = np.min(matrix,0)
    maxes = np.max(matrix,0)
    ranges = maxes - mins
    return ((matrix - averages)/ranges)


def run_regression(X, Y, X_test, Y_test, lambda_value = 0.1, normalize=False, batch_size=2700):
    x_train = normalize_data(X) if normalize else X
    y_train = Y
    x_test = X_test
    y_test = Y_test
    session = tf.Session()

    # Calculate number of features for X and Y
    x_features_length = len(X[0])
    y_features_length = len(Y[0])

    # Build Tensorflow graph parts
    x = tf.placeholder('float', [None, x_features_length], name="X")
    y = tf.placeholder('float', [None, y_features_length], name="Y")
    theta = tf.Variable(tf.random_normal([x_features_length, y_features_length], stddev=0.01), name="Theta")


    lambda_val = tf.constant(lambda_value)

    # Trying to implement this way http://openclassroom.stanford.edu/MainFolder/DocumentPage.php?course=MachineLearning&doc=exercises/ex5/ex5.html
    y_predicted = tf.matmul(x, theta, name="y_predicted")
    regularization_cost_part = tf.cast(tf.mul(lambda_val,tf.reduce_sum(tf.pow(theta,2)), name="regularization_param"), 'float')
    polynomial_cost_part = tf.reduce_sum(tf.pow(tf.sub(y_predicted, y), 2), name="polynomial_sum")

    # Set up some summary info to debug
    with tf.name_scope('cost') as scope:
        cost_func = tf.mul(1.0/batch_size, tf.cast(tf.add(polynomial_cost_part, regularization_cost_part), 'float'))
        cost_summ = tf.scalar_summary("cost", cost_func)

    training_func = tf.train.GradientDescentOptimizer(1.0).minimize(polynomial_cost_part)

    with tf.name_scope("test") as scope:
        correct_prediction = tf.sub(tf.cast(1, 'float'), tf.reduce_mean(tf.sub(y_predicted, y)))
        accuracy = tf.cast(correct_prediction, "float")
        accuracy_summary = tf.scalar_summary("accuracy", accuracy)

    saver = tf.train.Saver()
    merged = tf.merge_all_summaries()
    writer = tf.train.SummaryWriter("/tmp/football_logs", session.graph_def)
    init = tf.initialize_all_variables()

    session.run(init)
    for i in range(0, (len(x_train)/batch_size)):
        session.run(training_func, feed_dict={x: x_train[i*batch_size:i*batch_size+batch_size], y: y_train[i*batch_size:i*batch_size+batch_size]})
        if i % batch_size == 0:
            result = session.run([merged, accuracy], feed_dict={x: x_test, y: y_test})
            writer.add_summary(result[0], i)
            print "step %d, training accuracy %g"%(i, result[1])

    print "test accuracy %g"%session.run(accuracy, feed_dict={x: x_test, y: y_test})

    for i in xrange(1,100):
        print "%ith prediction \nexpected: %s \n actual: %s\n**************************************************************" % (i, y_test[i] ,session.run(y_predicted, feed_dict={x: [x_test[i]] }))

    save_path = saver.save(session, "/tmp/football.ckpt")
    print "Model saved in file: ", save_path
    session.close()
