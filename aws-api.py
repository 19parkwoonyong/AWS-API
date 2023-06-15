import boto3
import io
from PIL import Image, ImageDraw


def detect_labels(photo, bucket):

    # 내 aws 정보 연동
    client = boto3.client('rekognition', aws_access_key_id="my access key", 
        aws_secret_access_key="secret access key", 
        region_name="ap-northeast-2")

    # s3에서 이미지 갖고오기
    s3_connection = boto3.resource('s3', aws_access_key_id='access key', aws_secret_access_key='secret', region_name='ap-northeast-2')
    s3_object = s3_connection.Object(bucket, photo)
    s3_response = s3_object.get()

    stream = io.BytesIO(s3_response['Body'].read())
    image = Image.open(stream)

    # detect label 호출
    response = client.detect_labels(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})

    imgWidth, imgHeight = image.size
    draw = ImageDraw.Draw(image)

    # 인식범위 설정
    center_x = imgWidth / 2
    center_y = imgHeight / 2
    half_width = imgWidth / 4
    half_height = imgHeight / 4
    left_bound = center_x - half_width
    right_bound = center_x + half_width
    top_bound = center_y + half_height
    under_bound = center_y - half_height

    print('Detected labels for ' + photo)
    for label in response['Labels']:
        print(label['Name'] + ' : ' + str(label['Confidence']))
        if 'Instances' in label:
            for instance in label['Instances']:
                box = instance['BoundingBox']
                left = imgWidth * box['Left']
                top = imgHeight * box['Top']
                width = imgWidth * box['Width']
                height = imgHeight * box['Height']

                box_center_x = left + width / 2
                box_center_y = top + height / 2

                if left_bound <= box_center_x <= right_bound:
                    if under_bound <= box_center_y <= top_bound:

                        print('Left: ' + '{0:.0f}'.format(left))
                        print('Top: ' + '{0:.0f}'.format(top))
                        print('Label Width: ' + "{0:.0f}".format(width))
                        print('Label Height: ' + "{0:.0f}".format(height))

                        points = (
                            (left, top),
                            (left + width, top),
                            (left + width, top + height),
                            (left, top + height),
                            (left, top)
                        )
                        draw.line(points, fill='#00d400', width=2)

        

    image.show()
    return len(response['labels'])


def main():
    bucket = "zerash"
    photo = "uk.JPG"
    labels_count = detect_labels(photo, bucket)
    print("labels detected: " + str(labels_count))


if __name__ == "__main__":
    main()