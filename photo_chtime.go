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

	checkMark = "✓"
	xMark     = "✗"
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

	fmt.Println("")

	for _, f := range files {
		mark, result := action(fPath, f, tz, apply)
		fmt.Println(mark, result)
	}

	fmt.Printf("\nApplied: %t\n\n", apply)
}

func action(fPath string, f os.FileInfo, tz string, apply bool) (string, string) {
	var result string

	fn := f.Name()
	result += fn
	if fn[len(fn)-3:] != "jpg" && fn[len(fn)-3:] != "mp4" && fn[len(fn)-3:] != "gif" {
		result += " -> " + "skipped"
		if f.IsDir() {
			result += " (DIR)"
		}
		return xMark, result
	}
	tt := strings.Split(f.Name()[4:len(fn)-4], "_")
	ttt := tt[0] + "_T" + tt[1] + tz
	result += " -> " + ttt

	t, err := time.Parse(timeLayout, ttt)
	if err != nil {
		result += " -> " + err.Error()
		return xMark, result
	}
	result += " -> " + t.String()

	fnN := t.Format(timeLayoutR) + "_" + fn
	result += " -> " + fnN

	if apply {
		err = os.Chtimes(path.Join(fPath, fn), time.Now(), t)
		if err != nil {
			result += " -> " + err.Error()
			return xMark, result
		}
		err = os.Rename(path.Join(fPath, fn), path.Join(fPath, fnN))
		if err != nil {
			result += " -> " + err.Error()
			return xMark, result
		}
	}

	return checkMark, result
}
