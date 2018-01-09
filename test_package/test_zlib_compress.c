#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#include <zlib.h>

#define SRC_BUF_SIZE 2048

int main(int argc, char** argv) {
    printf("Zlib version => %s\n", ZLIB_VERSION);

    srand(time(NULL));

    char* src_buf = malloc(SRC_BUF_SIZE);
    if (src_buf == NULL) {
        printf("Allocate src_buf failed, size => %lu\n", SRC_BUF_SIZE);
        exit(EXIT_FAILURE);
    }
    for (int i = 0; i < SRC_BUF_SIZE; i++) {
        *(src_buf + i) = (char) rand();
    }
    
    const uLong compress_buf_size = compressBound(SRC_BUF_SIZE);
    char* compress_buf = calloc(1, compress_buf_size);
    if (compress_buf == NULL) {
        printf("Allocate compress_buf failed, size => %lu\n", compress_buf_size);
        exit(EXIT_FAILURE);
    }
    uLongf compressed_size = compress_buf_size;
    int res = compress(compress_buf, &compressed_size, src_buf, SRC_BUF_SIZE);
    if (res != Z_OK) {
        printf("Compress failed, res => %d\n", res);
        exit(EXIT_FAILURE);
    }
    printf("Original size => %lu, compressed size => %lu\n", SRC_BUF_SIZE, compressed_size);
    
    char* uncompress_buf = calloc(1, SRC_BUF_SIZE);
    if (compress_buf == NULL) {
        printf("Allocate uncompress_buf failed, size => %lu\n", SRC_BUF_SIZE);
        exit(EXIT_FAILURE);
    }
    uLongf uncompressed_size = SRC_BUF_SIZE;
    res = uncompress(uncompress_buf, &uncompressed_size, compress_buf, compressed_size);
    if (res != Z_OK) {
        printf("Uncompress failed, res => %d\n", res);
        exit(EXIT_FAILURE);
    }
    
    if (uncompressed_size != SRC_BUF_SIZE) {
        printf("Invalid uncompress, source size => %lu, uncompressed size => %lu\n", SRC_BUF_SIZE, uncompressed_size);
        exit(EXIT_FAILURE);
    } else if (memcmp(src_buf, uncompress_buf, SRC_BUF_SIZE) != 0) {
        printf("Invalid uncompress, source and uncompressed data not equal.\n");
        exit(EXIT_FAILURE);
    }
    
    printf("Compress / uncompress OK\n");

    free(src_buf);
    free(compress_buf);
    free(uncompress_buf);
    return EXIT_SUCCESS;
}
