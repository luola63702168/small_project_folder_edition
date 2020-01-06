package main

import (
	"fmt"
	"net/http"
	"os"
	"path"
	"regexp"
	"strconv"
	"sync"
)

// Requirements: multitask crawl all the photos on the first page of each post

// Step: make a request, get the list page,
// Go to the details page and get the url, at the end of jpg
// Request the url, to get the resp, save file

var wg sync.WaitGroup


// Tool function, which returns the content corresponding to url
func HandleUrl(url string) (Content string) {
	resp, _ := http.Get(url)
	defer resp.Body.Close()
	buf := make([]byte, 4*1024)
	for {
		n, _ := resp.Body.Read(buf)
		if n == 0 {
			break
		}
		Content += string(buf[:n])
	}
	return Content
}

// Tool function, saving pictures
func SaveImage(imageUrl string) {
	resp, _ := http.Get(imageUrl)
	filePath := "E:\\spiderImages2\\美女"+path.Base(imageUrl)
	f, _ := os.Create(filePath)
	defer f.Close()
	defer resp.Body.Close()

	buf := make([]byte, 4*1024)
	for {
		n, _ := resp.Body.Read(buf)
		if n==0{
			fmt.Println("文件保存完毕")
			wg.Done()
			break
		}
		_, _ = f.Write(buf[:n])
	}
}

// Process each detail page and extract the url corresponding to the photo
func HandleDetail(detailUrl string) {
	detailContent := HandleUrl(detailUrl)
	reg := regexp.MustCompile("<img class=\"BDE_Image\" src=\".*?\" size=")
	imageTempSlice := reg.FindAllString(detailContent, -1)
	reg2 := regexp.MustCompile("http.*jpg")
	for _, i := range imageTempSlice {
		imgUrl := reg2.FindString(i)
		go SaveImage(imgUrl)
		wg.Add(1)
	}
	wg.Done()
}

// Process each list page and extract the details page url
func HandleListContent(listContent string) {
	reg := regexp.MustCompile("<a rel=\"noreferrer\" href=\"/p/\\d{10}")
	resultSlice := reg.FindAllString(listContent, -1)
	reg2 := regexp.MustCompile("\\d{10}")
	seedUrl := "https://tieba.baidu.com/p/"
	for _, i := range resultSlice {
		go HandleDetail(seedUrl + reg2.FindString(i))
		wg.Add(1)
	}
	wg.Done()
}

// Build the url for each list page
func runListUrl() {
	startUrl := "https://tieba.baidu.com/f?kw=%E7%88%86%E7%85%A7&ie=utf-8&pn="
	for i := 0; i < 150; i += 50 {
		startUrl += strconv.Itoa(i)
		Content := HandleUrl(startUrl)
		go HandleListContent(Content)
		wg.Add(1)
	}
	wg.Wait()
}

func main() {
	runListUrl()
}