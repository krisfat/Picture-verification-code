
import math
import operator
from functools import reduce
from time import sleep

import requests
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from io import BytesIO

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def download_img():
	# 从网站上获取图片
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'
	}
	url = 'http://www.1kkk.com/image3.ashx'
	# 取大约500张图片，其实最后终极去重之后只剩下了150张左右
	for count in range(1, 501):
		response = requests.get(url, headers=headers)
		if response.status_code == 200:
			img = response.content
			with open('./imgs/image%d.jpg' % count, 'bw') as f:
				f.write(img)
			print(count, 'Done !')
			cut_img()


def cut_img():
	# 将图片取第一排，切割成4小块
	nums = 0
	for x in range(1, 201):
		for y in range(1,5):
			nums += 1
			img = Image.open('./imgs/image%s.jpg' % x)
			img = img.crop((76 * (y-1), 0, 76 * y, 76))
			img.save('./images/image%s.jpg'% nums)


def compare():
	# 对比图片达到去重的目的，这里为了写的更为详细，其实写的有点麻烦了可以改良的
	x = 1
	while True:
		y = x +1
		try:
			img1 = Image.open('。/images/image%s.jpg' % x)
		except:
			x+=1
			if x > 800:
				break
			continue
		while True:
			try:
				img2 = Image.open('./images/image%s.jpg' % y)
			except:
				y += 1
				if y > 800:
					break
				continue
			h1 = img1.histogram()
			h2 = img2.histogram()
			result = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a - b) ** 2, h1, h2))) / len(h1))
			if result < 7:
				print(result, x, y)
				os.remove('./images/image%s.jpg' % y)
			y += 1
			if y > 800:
				break
		x += 1
		if x > 800:
			break


def get_img():
	# 从网站上获取当前页面的验证码
	url = 'http://www.1kkk.com/login/'
	browser.get(url)
	screenshot = browser.get_screenshot_as_png()
	screenshot = Image.open(BytesIO(screenshot))
	# crop中的数值收您分辨率的影响，所以请自己获取对应的坐标
	image1 = screenshot.crop((1402, 660, 1554, 812))
	image1 = image1.resize((76, 76))
	image1.save('./kkk/image1.png')
	image1 = screenshot.crop((1557, 660, 1709, 812))
	image1 = image1.resize((76, 76))
	image1.save('./kkk/image2.png')
	image1 = screenshot.crop((1713, 660, 1865, 812))
	image1 = image1.resize((76, 76))
	image1.save('./kkk/image3.png')
	image1 = screenshot.crop((1870, 660, 2022, 812))
	image1 = image1.resize((76, 76))
	image1.save('./kkk/image4.png')


def login(result):
	# 通过拿到的结果进行点击旋转的操作
	for x in result.keys():
		images = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/section/div[2]/div/div/form/div/div[%d]' % (x + 1))))
		for y in range(result[x]):
			images.click()
			sleep(0.5)


def compare_images():
	# 将获取到的图片同本地的库进行比对
	result_list = {}
	for i in range(1, 5):
		for x in range(4):
			for j in range(1, len(os.listdir('./images'))):
				result = img_detail(i, j, x)
				if result:
					result_list[i] = 0 if x == 0 else 4 - x
					print(i, j, x)
					break
	return result_list


def img_detail(i, j, angle):
	# 对比两张图片的每一个像素点
	image1 = Image.open('/Users/krisfat/Python学习/5.爬虫/day6/kkk/image%d.png' % i)
	# rotate逆时针旋转
	image1 = image1.rotate(90 * angle)
	image2 = Image.open('/Users/krisfat/Python学习/5.爬虫/day6/images/image%d.jpg' % j)
	# 逐个像素点惊醒对比，出现不一样的直接返回
	for x in range(76):
		for y in range(76):
			pixel1 = image1.load()[x, y]
			pixel2 = image2.load()[x, y]
			threshold = 100
			if not abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
				return False
	return True


def rename():
	# 去重之后对图片进行重命名
	i = 1
	for x in range(1, 676):
		try:
			os.rename('./images/image%d.jpg'%x, './images/image%d.jpg'%i)
		except:
			continue
		i += 1


def main():
	# 下载图片运行一次就行
	# download_img()
	# 切割图片运行一次就行
	# cut_img()
	# 去重也只需要运行一次
	# compare()
	# 在登录的时候获取网页上的图片
	# get_img()
	# 去重之后使用进行重命名
	rename()
	# 得到字典key是第几张对图片，value是对应的旋转次数
	# result = compare_images()
	# 实现点击旋转
	# login(result)
	print('Done !')


if __name__ == '__main__':
	main()
