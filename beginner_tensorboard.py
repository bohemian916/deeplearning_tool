from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

import tensorflow as tf
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W)+b)
y_ = tf.placeholder(tf.float32, [None, 10])

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

# tensorboard
w_hist = tf.histogram_summary("weights", W)
b_hist = tf.histogram_summary("biases", b)
y_hist = tf.histogram_summary("y", y)

correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float32"))

with tf.name_scope("train") as scope:
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
    acc_summary_train = tf.scalar_summary("train_acc", accuracy)
    loss_summary_train = tf.scalar_summary("cross_entropy_train", cross_entropy)


with tf.name_scope("val") as scope:
    acc_summary_val = tf.scalar_summary("val_acc", accuracy)
    loss_summary_val = tf.scalar_summary("cross_entropy_val", cross_entropy)


init = tf.initialize_all_variables()
sess = tf.Session()
sess.run(init)

merged = tf.merge_all_summaries()
writer = tf.train.SummaryWriter("data", sess.graph_def)

for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x:batch_xs, y_:batch_ys})
    
    if i%10==0:
        train_list = [accuracy, acc_summary_train, loss_summary_train, w_hist, b_hist, y_hist]
        result = sess.run(train_list, feed_dict={x:batch_xs, y_:batch_ys})
        for j in range(1,len(result)): 
            writer.add_summary(result[j], i)
        print("Train accuracy at step %s: %s" % (i, result[0]))

        val_list = [accuracy,acc_summary_val, loss_summary_val]
        result = sess.run(val_list, feed_dict={x:mnist.validation.images, y_:mnist.validation.labels})
        for j in range(1,len(result)): 
            writer.add_summary(result[j], i)

        print("Validation accuracy at step %s: %s" % (i, result[0]))


#print "test"  + str(sess.run(accuracy2, feed_dict={x:mnist.test.images, y_:mnist.test.labels}))

