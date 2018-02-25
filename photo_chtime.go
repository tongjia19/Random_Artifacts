package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strings"
	"time"
)

const (
	timeLayout  = "20060102_T150405Z07:00"
	timeLayoutR = "2006-01-02-15-04-05"

	ottawaTZ  = "-05:00"
	beijingTZ = "+08:00"
)

func main() {
	path := os.Args[1]

	apply := false
	if len(os.Args) > 2 {
		if os.Args[2] == "a" {
			apply = true
		}
	}

	files, err := ioutil.ReadDir(path)
	if err != nil {
		log.Fatal(err)
	}

	for _, f := range files {
		fn := f.Name()
		if fn[len(fn)-3:] != "jpg" && fn[len(fn)-3:] != "mp4" && fn[len(fn)-3:] != "gif" {
			continue
		}
		tt := strings.Split(f.Name()[4:len(fn)-4], "_")
		ttt := tt[0] + "_T" + tt[1] + beijingTZ

		t, err := time.Parse(timeLayout, ttt)
		if err != nil {
			fmt.Println(err)
		}

		fnN := t.Format(timeLayoutR) + "_" + fn

		fmt.Println(fn, "->", ttt, "->", t, "->", fnN)

		if apply {
			os.Chtimes(path+fn, time.Now(), t)
			os.Rename(path+fn, path+fnN)
		}
	}

	fmt.Println("Applied:", apply)
}
