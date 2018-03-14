#!/bin/bash
echo "开始爬取安居客"
scrapy crawl anjuke
echo "开始爬取搜房网"
scrapy crawl fang
echo "开始爬取新浪乐居"
scrapy crawl leju
echo "开始爬取腾讯地产"
scrapy crawl qq