import tensorflow as tf
import numpy as np

def normalize_data(matrix):
    averages = np.average( matrix, 0)
    mins = np.min( matrix,0 )
    maxes = np.max( matrix, 0)
    ranges = maxes - mins

    # handle divide by zero issues by setting to 0 (only happens when max-min = 0)
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide((matrix - averages), ranges)
        c[c == np.inf] = 0
        c = np.nan_to_num(c)

    return c.tolist()


def create_placeholder(data, type='float', name=''):
    data_length = len(data[0])
    return tf.placeholder(type, [None, data_length], name=name)


def build_theta(input, output, name=''):
    input_length = len(input[0])
    output_length = len(output[0])
    return tf.Variable(tf.random_normal([input_length, output_length], stddev=0.01), name=name)


def polynomial_features(X_in, degree=2):
    for i in range(2,degree + 1):
        x_pow = np.power(X_in, i)
        x_out = np.concatenate((X_in,x_pow), 1)

    return x_out.tolist()


def run_regression(x_train, y_train, x_test, y_test, lambda_value = 0.1, normalize=False, polynomial=False, degree=2,batch_size=2700):
    if polynomial:
        x_train = polynomial_features(x_train, degree=degree)
        x_test = polynomial_features(x_test, degree=degree)   

    if normalize:
        x_train = normalize_data(x_train)
        x_test = normalize_data(x_test)

    session = tf.Session()

    # Build Tensorflow placeholders
    x = create_placeholder(x_train, name="X")
    y = create_placeholder(y_train, name="Y")

    # adjustment to predictions that are negative
    y_min = tf.zeros([1, len(y_train[0])], dtype=tf.float32)

    # prediction variables
    theta = build_theta( x_train, y_train, name="Theta")
    y_predicted = tf.maximum(tf.matmul(x, theta, name="y_predicted"), y_min)

    # Set up some summary info to debug
    with tf.name_scope('cost') as scope:
        cost_func = tf.reduce_mean(tf.pow(y_predicted - y,2))
        cost_summ = tf.scalar_summary("cost", cost_func)

    training_func = tf.train.GradientDescentOptimizer(10.0).minimize(cost_func)

    saver = tf.train.Saver()
    merged = tf.merge_all_summaries()
    writer = tf.train.SummaryWriter("/tmp/football_logs", session.graph_def)
    init = tf.initialize_all_variables()

    session.run(init)
    for i in range(0, 50000):
        session.run(training_func, feed_dict={x: x_train, y: y_train})
        if i % 1000 == 0:
            result = session.run([merged, cost_func], feed_dict={x: x_train, y: y_train})
            writer.add_summary(result[0], i)
            print "step %d, training accuracy %g"%(i, result[1])

    print "test accuracy %g"%session.run(cost_func, feed_dict={x: x_test, y: y_test})

    for i in xrange(1,10):
        diff = tf.to_int32(tf.sub(y_predicted, y_test[i]))
        result = session.run([y_predicted, diff], feed_dict={x: [x_test[i]] })
        print "%ith prediction \nexpected: %s \nactual: %s\ndiff: %s\n**************************************************************" % (i, y_test[i] ,result[0], result[1])

    save_path = saver.save(session, "/tmp/football.ckpt")
    print "Model saved in file: ", save_path
    session.close()
