package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path"
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
	tz := ottawaTZ

	fPath := os.Args[1]

	apply := false
	if len(os.Args) > 2 {
		if os.Args[2] == "a" {
			apply = true
		}
	}

	files, err := ioutil.ReadDir(fPath)
	if err != nil {
		log.Fatal(err)
	}

	for _, f := range files {
		fn := f.Name()
		if fn[len(fn)-3:] != "jpg" && fn[len(fn)-3:] != "mp4" && fn[len(fn)-3:] != "gif" {
			fmt.Println("Skipped:", fn)
			continue
		}
		tt := strings.Split(f.Name()[4:len(fn)-4], "_")
		ttt := tt[0] + "_T" + tt[1] + tz

		t, err := time.Parse(timeLayout, ttt)
		if err != nil {
			fmt.Println(err)
			continue
		}

		fnN := t.Format(timeLayoutR) + "_" + fn

		fmt.Println(fn, "->", ttt, "->", t, "->", fnN)

		if apply {
			err = os.Chtimes(path.Join(fPath, fn), time.Now(), t)
			if err != nil {
				fmt.Println(err)
				continue
			}
			err = os.Rename(path.Join(fPath, fn), path.Join(fPath, fnN))
			if err != nil {
				fmt.Println(err)
				continue
			}
		}
	}

	fmt.Println("Applied:", apply)
}
