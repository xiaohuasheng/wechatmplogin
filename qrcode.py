import requests


def save_qrcode():
    main_host = 'task.xiaohuasheng.cc'
    # main_host = 'localhost:9091'
    url = f'http://{main_host}/api/chatgpt?text_type=qrcode'
    # Create a dictionary with the file to be uploaded
    files = {'file': ('qrcode.png', open('qrcode.png', 'rb'))}

    # Make the POST request
    response = requests.post(url, files=files)

    # Check the response
    if response.status_code == 200:
        print("File upload successful")
        print(response.text)
    else:
        print("File upload failed")
        print(response.status_code, response.text)
        return False
    return True


if __name__ == '__main__':
    save_qrcode()
