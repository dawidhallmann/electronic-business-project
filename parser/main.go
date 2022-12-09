package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

type Product struct {
	Link       string            `json:"link"`
	Name       string            `json:"name"`
	Price      string            `json:"price"`
	Properties map[string]string `json:"propertys"`
	Variants   map[string]any    `json:"variants"`
	Category   string            `json:"category"`
	ImageLink  string            `json:"image_high_quality_link"`
}

func main() {
	jsonFile, err := os.Open("../scraper/data/products.json")
	if err != nil {
		panic("opening file failed")
	}

	defer jsonFile.Close()

	products := parseFile(jsonFile)
	categoriesSlice := make([]string, 0)

	for _, product := range products {
		categoriesSlice = append(categoriesSlice, product.Category)
	}

	writeCategories(categoriesSlice)
	writeProducts(products)
}

func parseFile(f *os.File) (products []Product) {
	byteValue, err := ioutil.ReadAll(f)
	if err != nil {
		panic("reading file failed")
	}

	if err = json.Unmarshal(byteValue, &products); err != nil {
		panic("Unmarshalling json failed")
	}

	return products
}

func writeCategories(categories []string) {
	header := "Category ID;Active (0/1);Name *;Parent category;Root category (0/1);Description;Meta title;Meta keywords;Meta description;URL rewritten;Image URL\n"
	destination := "categories.csv"
	categoryID := 3
	categoriesMap := make(map[string]int)

	outputFile, err := os.Create(destination)
	if err != nil {
		panic("creating file failed")
	}

	defer outputFile.Close()

	outputFile.WriteString(header)

	for _, category := range categories {
		if _, ok := categoriesMap[category]; !ok {
			str := fmt.Sprintf("%v;1;%v;Strona główna;0;;;;;;\n", categoryID, category)
			categoryID += 1
			categoriesMap[category] = categoryID

			outputFile.WriteString(str)
		}
	}
}

func writeProducts(products []Product) {
	header := "ID;Aktywny (0 lub 1);Nazwa*;Kategorie (x,y,z...);Cena zawiera podatek. (brutto);ID reguły podatku;W sprzedaży (0 lub 1);Ilość;Podsumowanie;Opis;Etykieta, gdy w magazynie;Pokaż cenę (0 = Nie, 1 = Tak);Adresy URL zdjęcia (x,y,z...);Usuń istniejące zdjęcia (0 = Nie, 1 = Tak);Cecha(Nazwa:Wartość:Pozycja:Indywidualne);Dostępne tylko online (0 = Nie, 1 = Tak);Stan;Konfigurowalny (0 = Nie, 1 = Tak);Można wgrywać pliki (0 = Nie, 1 = Tak);Pola tekstowe (0 = Nie, 1 = Tak);Wirtualny produkt (0 = No, 1 = Yes);Przepisany URL\n"
	destination := "products.csv"
	taxRuleID := 1

	outputFile, err := os.Create(destination)
	if err != nil {
		panic("creating file failed")
	}

	defer outputFile.Close()

	outputFile.WriteString(header)

	for id, product := range products {
		price := strings.ReplaceAll(strings.ReplaceAll(strings.Trim(product.Price, " zł"), ",", "."), " ", "")
		name := trimProductName(strings.ReplaceAll(strings.ReplaceAll(strings.ReplaceAll(strings.ReplaceAll(strings.ReplaceAll(product.Name, ";", " "), ",", " "), "  ", " "), "?", ""), "=", ""))
		url := newUrl(name)
		properies := newProperties(product.Properties)

		outputFile.WriteString(fmt.Sprintf("%v;1;%v;%v;%v;%v;0;10;Podsumowanie;Opis;W magazynie;1;%v;1;%v;0;new;0;0;0;0;%v\n", id+50, name, product.Category, price, taxRuleID, product.ImageLink, properies, url))
	}
}

func trimProductName(str string) string {
	if len(str) > 127 {
		spaceSlice := strings.Split(str, " ")
		str = ""

		for n := 0; n < len(spaceSlice)-1; n += 1 {
			str += spaceSlice[n] + " "
		}

		str = strings.TrimSuffix(str, " ")

		if len(str) > 127 {
			str = trimProductName(str)
		}
	}

	return str
}

func newUrl(name string) string {
	url := strings.ReplaceAll(name, " ", "_")
	if len(url) > 64 {
		url = url[0:64]
	}

	return url
}

func newProperties(properties map[string]string) (propertiesStr string) {
	position := 1

	for key, val := range properties {
		val = strings.ReplaceAll(strings.ReplaceAll(strings.ReplaceAll(strings.ReplaceAll(strings.ReplaceAll(val, "\n", " "), ",", " "), ":", ""), "   ", "  "), "  ", " ")
		propertiesStr += fmt.Sprintf("%v:%v:%v,", key, val, position)
		position += 1
	}

	return strings.TrimSuffix(propertiesStr, ",")
}
