package main

import "fmt"

func slidingDotProduct(a []int, b []int) int {
	var sum int
	for i := 0; i < len(a); i++ {
		sum += a[i] * b[i]
	}
	return sum
}

func main() {
	// Create an array of ints with a length of 3
	var kernel = []int{1, 3, 2}

	var signal = []int{0, 0, 0, 4, 5, 0, 0, 0, 0, 1, 2, 3}

	// reverse kernel
	var convolution = make([]int, len(kernel))
	for i := len(kernel) - 1; i >= 0; i-- {
		convolution[len(kernel)-i-1] = kernel[i]
	}

	// iterate over the signal with the convolution
	for i := 0; i < len(signal); i++ {
		fmt.Println(slidingDotProduct(signal[i:i+len(convolution)], convolution))
	}

	// print kernel
	fmt.Println(kernel)
	// print signal
	fmt.Println(signal)
}
