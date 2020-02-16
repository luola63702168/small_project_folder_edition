import tensorflow as tf
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

FLAGS = tf.app.flags.FLAGS
tf.app.flags.DEFINE_string("tfrecords_dir", "./tfrecords/captcha.tfrecords", "验证码tfrecords文件")
tf.app.flags.DEFINE_string("captcha_dir", r"E:\mac_obj_file\GenPics2", "验证码图片路径")
tf.app.flags.DEFINE_string("labels", r"E:\mac_obj_file\GenPics2\lab.csv", "验证码labels_csv文件路径")
tf.app.flags.DEFINE_string("letter", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "验证码字符的种类")


def dealwithlabel(label_str):
    """处理lab数据，将字母转换为列表
    参考：[[13, 25, 15, 15], [22, 10, 7, 10], [22, 15, 18, 9], [16, 6, 13, 10], [1, 0, 8, 17], [0, 9, 24, 14].....]

    """
    num_letter = dict(enumerate(list(FLAGS.letter)))
    letter_num = dict(zip(num_letter.values(), num_letter.keys()))
    print(letter_num)
    array = []
    for string in label_str:
        letter_list = []
        for letter in string.decode('utf-8'):
            letter_list.append(letter_num[letter])
        array.append(letter_list)
    print(array)
    label = tf.constant(array)
    return label


def get_captcha_image():
    """
    获取验证码图片数据
    :param file_list: 路径+文件名列表
    :return: image
    """
    filename = []
    for i in range(6000):
        string = str(i) + ".jpg"
        filename.append(string)
    file_list = [os.path.join(FLAGS.captcha_dir, file) for file in filename]
    file_queue = tf.train.string_input_producer(file_list, shuffle=False)
    reader = tf.WholeFileReader()
    key, value = reader.read(file_queue)
    image = tf.image.decode_jpeg(value)
    image.set_shape([20, 80, 3])
    image_batch = tf.train.batch([image], batch_size=6000, num_threads=1, capacity=6000)
    return image_batch


def get_captcha_label():
    """
    读取验证码图片标签数据
    :return: label_batch ：[["NZPP"], ["WKHK"], ["ASDY"]]
    """
    file_queue = tf.train.string_input_producer([FLAGS.labels], shuffle=False)
    reader = tf.TextLineReader()
    key, value = reader.read(file_queue)
    records = [[1], ["None"]]
    number, label = tf.decode_csv(value, record_defaults=records)
    label_batch = tf.train.batch([label], batch_size=6000, num_threads=1, capacity=6000)
    return label_batch


def write_to_tfrecords(image_batch, label_batch):
    """
    将图片内容和标签写入到tfrecords文件当中
    :param image_batch: 特征值
    :param label_batch: 标签纸
    :return: None
    """
    label_batch = tf.cast(label_batch, tf.uint8)
    print(label_batch)
    writer = tf.python_io.TFRecordWriter(FLAGS.tfrecords_dir)
    for i in range(6000):
        image_string = image_batch[i].eval().tostring()
        label_string = label_batch[i].eval().tostring()
        example = tf.train.Example(features=tf.train.Features(feature={
            "image": tf.train.Feature(bytes_list=tf.train.BytesList(value=[image_string])),
            "label": tf.train.Feature(bytes_list=tf.train.BytesList(value=[label_string]))
        }))
        writer.write(example.SerializeToString())
    writer.close()
    return None


if __name__ == "__main__":
    i = input("你确定要生成文件吗？确定请输入：1，否则请输入0 ：")
    if i == "0":
        import sys
        sys.exit(1)
    else:
        image_batch = get_captcha_image()
        label = get_captcha_label()
        print(image_batch, label)
        with tf.Session() as sess:
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)
            label_str = sess.run(label)
            print(label_str)
            label_batch = dealwithlabel(label_str)
            print(label_batch)
            write_to_tfrecords(image_batch, label_batch)
            coord.request_stop()
            coord.join(threads)
