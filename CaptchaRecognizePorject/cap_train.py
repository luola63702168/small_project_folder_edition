import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string("captcha_dir", "./tfrecords/captcha.tfrecords", "验证码数据的路径")
tf.app.flags.DEFINE_integer("batch_size", 100, "每批次训练的样本数")
tf.app.flags.DEFINE_integer("label_num", 4, "每个样本的目标值数量")
tf.app.flags.DEFINE_integer("letter_num", 26, "每个目标值取的字母的可能心个数")


def weight_variables(shape):
    """根据形状初始化权重"""
    w = tf.Variable(tf.random_normal(shape=shape, mean=0.0, stddev=1.0))
    return w


def bias_variables(shape):
    """根据形状初始化偏置"""
    b = tf.Variable(tf.constant(0.0, shape=shape))
    return b


def read_and_decode():
    """
    读取验证码数据API
    :return: image_batch, label_batch
    """
    file_queue = tf.train.string_input_producer([FLAGS.captcha_dir])
    reader = tf.TFRecordReader()
    key, value = reader.read(file_queue)
    features = tf.parse_single_example(value, features={
        "image": tf.FixedLenFeature([], tf.string),
        "label": tf.FixedLenFeature([], tf.string),
    })
    image = tf.decode_raw(features["image"], tf.uint8)
    label = tf.decode_raw(features["label"], tf.uint8)
    image_reshape = tf.reshape(image, [20, 80, 3])
    label_reshape = tf.reshape(label, [4])
    print(image_reshape, label_reshape)
    image_batch, label_btach = tf.train.batch([image_reshape, label_reshape], batch_size=FLAGS.batch_size,
                                              num_threads=1, capacity=FLAGS.batch_size)
    print(image_batch, label_btach)
    return image_batch, label_btach


def fc_model(image):
    """
    进行预测结果
    :param image: 100图片特征值[100, 20, 80, 3]
    :return: y_predict预测值[100, 4 * 26]
    """
    with tf.variable_scope("model"):
        image_reshape = tf.reshape(image, [-1, 20 * 80 * 3])
        weights = weight_variables([20 * 80 * 3, 4 * 26])
        bias = bias_variables([4 * 26])
        # [100, 4 * 26]
        y_predict = tf.matmul(tf.cast(image_reshape, tf.float32), weights) + bias

    return y_predict


def predict_to_onehot(label):
    """
    将读取文件当中的目标值转换成one-hot编码
    :param label: [100, 4]      [[13, 25, 15, 15], [19, 23, 20, 16]......]
    :return: one-hot
    """
    label_onehot = tf.one_hot(label, depth=FLAGS.letter_num, on_value=1.0, axis=2)
    print(label_onehot)
    return label_onehot


def captcharec():
    """
    验证码识别程序
    :return:
    """
    # 1、 获取数据
    image_batch, label_batch = read_and_decode()
    # 2、建立模型（单层）
    y_predict = fc_model(image_batch)
    #  [100, 4 * 26]
    print(y_predict)
    # 3、目标值转换成one-hot编码 [100, 4, 26]
    y_true = predict_to_onehot(label_batch)
    # 4、softmax计算, 交叉熵损失计算
    with tf.variable_scope("soft_cross"):
        # 求平均交叉熵损失 ,y_true [100, 4, 26]--->[100, 4*26]
        loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
            labels=tf.reshape(y_true, [FLAGS.batch_size, FLAGS.label_num * FLAGS.letter_num]),
            logits=y_predict))
    # 5、梯度下降优化损失
    with tf.variable_scope("optimizer"):
        train_op = tf.train.GradientDescentOptimizer(0.01).minimize(loss)
    # 6、准确率
    with tf.variable_scope("acc"):
        # 比较每个预测值和目标值是否位置(4)一样    y_predict： [100, 4 * 26]---->[100, 4, 26]
        equal_list = tf.equal(tf.argmax(y_true, 2),
                              tf.argmax(tf.reshape(y_predict, [FLAGS.batch_size, FLAGS.label_num, FLAGS.letter_num]),
                                        2))
        # equal_list：length：100 --> [1, 0, 1, 0, 1, 1,..........]
        accuracy = tf.reduce_mean(tf.cast(equal_list, tf.float32))
    init_op = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init_op)
        # 线程
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(sess, coord=coord)
        # 训练
        for i in range(5000):
            sess.run(train_op)
            # print("第%d批次的准确率为：%f" % (i, accuracy.eval()))
            print("第%d批次的准确率为：%f" % (i, sess.run(accuracy)))
        # 回收线程
        coord.request_stop()
        coord.join(threads)
    return None


if __name__ == "__main__":
    captcharec()
