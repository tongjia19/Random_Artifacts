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
	checkMark = "✓"
	xMark     = "✗"

	timeLayoutCHTIME  = "20060102_T150405Z07:00"
	timeLayoutRCHTIME = "2006-01-02-15-04-05Z07:00"

	timeLayoutR = "2006-01-02-15-04-05"

	beijingTZ = "+08:00"

	ottawaEDTTZ = "-04:00"
	ottawaESTTZ = "-05:00"

	euroTZ = "+01:00"
)

var (
	// OTTAWA ..
	OTTAWA         = false
	ottawaEDTTS, _ = time.Parse("2006-01-02-15-04-05", "2018-03-10-03-00-00")
	ottawaEDTTE, _ = time.Parse("2006-01-02-15-04-05", "2018-11-03-02-00-00")

	// RENAME ..
	RENAME = true

	// RENAMED ..
	RENAMED = false

	// TZ ..
	TZ = euroTZ
)

func main() {
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

	var mark, result string
	for n, f := range files {
		if f.IsDir() || f.Name() == ".DS_Store" {
			continue
		}
		mark, result = action(fPath, f, TZ, apply)
		fmt.Println(mark, n, result)
	}

	fmt.Printf("\nApplied: %t\n\n", apply)
}

func action(fPath string, f os.FileInfo, tz string, apply bool) (string, string) {
	var err error
	var result string

	fn := f.Name()
	result += fn

	correctType, typee := checkFileType(fn)
	if !correctType {
		result += typee
		return xMark, result
	}

	var ttt string
	if RENAMED {
		if strings.Count(fn[:20], "-") == 5 {
			fn = fn[:19]
		}
		ttt = fn
	} else {
		if strings.Count(fn[:20], "-") == 5 {
			fn = fn[20:]
		}

		fn = cleanFilename(fn)
		result += " -> " + fn

		tt := strings.Split(fn[4:len(fn)-4], "_")
		if strings.Contains(fn, "PANO_") {
			fn = strings.Replace(fn, ".vr", "", 1)
			tt = strings.Split(fn[5:len(fn)-4], "_")
		}
		ttt = tt[0] + "_T" + tt[1]
	}
	result += " -> " + ttt

	tttz := ttt + tz
	var t time.Time
	if RENAMED {
		t, err = time.Parse(timeLayoutRCHTIME, tttz)
	} else {
		t, err = time.Parse(timeLayoutCHTIME, tttz)
	}
	if err != nil {
		result += " -> " + err.Error()
		return xMark, result
	}
	if OTTAWA {
		t = ottawaDST(t, ttt)
	}
	result += " -> " + t.String()

	var fnN string
	if !RENAMED && RENAME {
		fnN = (t.Format(timeLayoutR) + "_" + fn)
		result += " -> " + fnN
	}

	if apply {
		err = os.Chtimes(path.Join(fPath, f.Name()), time.Now(), t)
		if err != nil {
			result += " -> " + err.Error()
			return xMark, result
		}
		if !RENAMED && RENAME {
			err = os.Rename(path.Join(fPath, f.Name()), path.Join(fPath, fnN))
			if err != nil {
				result += " -> " + err.Error()
				return xMark, result
			}
		}
	}

	return checkMark, result
}

func actionCHTIME(fPath string, f os.FileInfo, tz string, apply bool) (string, string) {
	var result string

	fn := f.Name()
	result += fn

	correctType, typee := checkFileType(fn)
	if !correctType {
		result += typee
		return xMark, result
	}

	if strings.Count(fn[:20], "-") == 5 {
		fn = fn[:19]
	}
	ttt := fn
	result += " -> " + ttt

	tttz := ttt + tz
	t, err := time.Parse(timeLayoutRCHTIME, tttz)
	if err != nil {
		result += " -> " + err.Error()
		return xMark, result
	}
	if OTTAWA {
		t = ottawaDST(t, ttt)
	}
	result += " -> " + t.String()

	if apply {
		err = os.Chtimes(path.Join(fPath, f.Name()), time.Now(), t)
		if err != nil {
			result += " -> " + err.Error()
			return xMark, result
		}
	}

	return checkMark, result
}

func checkFileType(fn string) (bool, string) {
	fnExt := fn[len(fn)-3:]
	if !strings.EqualFold(fnExt, "jpg") &&
		!strings.EqualFold(fnExt, "png") &&
		!strings.EqualFold(fnExt, "gif") &&
		!strings.EqualFold(fnExt, "mp4") &&
		!strings.EqualFold(fnExt, "mov") &&
		!strings.EqualFold(fnExt, "3gp") {
		return false, " -> " + "skipped"
	}
	return true, ""
}

func cleanFilename(fn string) string {
	if strings.Contains(fn, "Burst_Cover_Collage_") {
		fn = strings.Replace(fn, "Burst_Cover_Collage_", "COL_", 1)
		fn = fn[:len(fn)-10] + "_" + fn[len(fn)-10:]
	} else if strings.Contains(fn, "Burst_Cover_GIF_Action_") {
		fn = strings.Replace(fn, "Burst_Cover_GIF_Action_", "GIF_", 1)
		fn = fn[:len(fn)-10] + "_" + fn[len(fn)-10:]
	} else if strings.Contains(fn, "_BURST") {
		fn = fn[14:]
		fn = strings.Replace(fn, "_BURST", "IMG_", 1)
		fn = strings.Replace(fn, "_COVER", "", 1)
		fn = fn[:len(fn)-10] + "_" + fn[len(fn)-10:]
	}
	return fn
}

func inTimeSpan(start, end, check time.Time) bool {
	return check.After(start) && check.Before(end)
}

func ottawaDST(t time.Time, ttt string) time.Time {
	if inTimeSpan(ottawaEDTTS, ottawaEDTTE, t) {
		TZ = ottawaEDTTZ
		tttz := ttt + TZ
		t, _ = time.Parse(timeLayoutRCHTIME, tttz)
	}
	return t
}
