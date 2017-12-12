#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#include <zlib.h>

#define SRC_BUF_SIZE 2048

int main(int argc, char** argv) {
    printf("Zlib version => %s\n", ZLIB_VERSION);
    srand(time(0));

    char* src_buf = malloc(SRC_BUF_SIZE);
    if (src_buf == NULL) {
        printf("Allocate src_buf failed, size => %lu\n", SRC_BUF_SIZE);
        exit(1);
    }
    for (int i = 0; i < SRC_BUF_SIZE; i++) {
        *(src_buf + i) = (char) rand();
    }
    
    const uLong compress_buf_size = compressBound(SRC_BUF_SIZE);
    char* compress_buf = calloc(1, compress_buf_size);
    if (compress_buf == NULL) {
        printf("Allocate compress_buf failed, size => %lu\n", compress_buf_size);
        exit(1);
    }
    uLongf compressed_size = compress_buf_size;
    int res = compress(compress_buf, &compressed_size, src_buf, SRC_BUF_SIZE);
    if (res != Z_OK) {
        printf("Compress failed, res => %d\n", res);
        exit(1);
    }
    printf("Original size => %lu, compressed size => %lu\n", SRC_BUF_SIZE, compressed_size);
    
    char* uncompress_buf = calloc(1, SRC_BUF_SIZE);
    if (compress_buf == NULL) {
        printf("Allocate uncompress_buf failed, size => %lu\n", SRC_BUF_SIZE);
        exit(1);
    }
    uLongf uncompressed_size = SRC_BUF_SIZE;
    res = uncompress(uncompress_buf, &uncompressed_size, compress_buf, compressed_size);
    if (res != Z_OK) {
        printf("Uncompress failed, res => %d\n", res);
        exit(1);
    }
    
    if (uncompressed_size != SRC_BUF_SIZE) {
        printf("Invalid uncompress, source size => %lu, uncompressed size => %lu\n", SRC_BUF_SIZE, uncompressed_size);
        exit(1);
    } else if (memcmp(src_buf, uncompress_buf, SRC_BUF_SIZE) != 0) {
        printf("Invalid uncompress, source and uncompressed data not equal.\n");
        exit(1);
    }
    
    printf("Compress / uncompress OK\n");

    free(src_buf);
    free(compress_buf);
    free(uncompress_buf);
    return 0;
}
