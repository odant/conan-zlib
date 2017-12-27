#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#include <zip.h>
#include <unzip.h>
#ifdef _WIN32
    #include <iowin32.h>
#endif

/* TODO: create test for this headers */
#include <crypt.h>
#include <mztools.h>

#define SRC_SIZE 1024 * 1024
const char* zip_fname = "test_minizip_compress.zip";

void init(void);
void fill_data(char*, size_t);

int print_zip_info(unzFile);
void Display64BitsSize(ZPOS64_T, int);

int main(int argc, char** argv) {

    init();

    /* Zip */
    printf("---------- Create ZIP ----------\n");

    zipFile zf = zipOpen64(zip_fname, APPEND_STATUS_CREATE);
    if (zf == NULL) {
        printf("Error in zipOpen64, fname => %s\n", zip_fname);
        exit(1);
    }
    
    char* src_data = malloc(SRC_SIZE);
    if (src_data == NULL) {
        printf("Can`t allocate source buffer\n");
        exit(1);
    }
    fill_data(src_data, SRC_SIZE);
    
    int err;
    zip_fileinfo zfi = {0};
    err = zipOpenNewFileInZip64(zf, "fname.bin", &zfi, NULL, 0, NULL, 0, NULL, Z_DEFLATED, Z_BEST_COMPRESSION, 0);
    if (err != ZIP_OK) {
        printf("Error in zipOpenNewFileInZip64, err => %d\n", err);
        exit(1);
    }
    
    err = zipWriteInFileInZip(zf, src_data, SRC_SIZE);
    if (err != ZIP_OK) {
        printf("Error in zipWriteInFileInZip, err => %d\n", err);
        exit(1);
    }
    
    err = zipCloseFileInZip(zf);
    if (err != ZIP_OK) {
        printf("Error in zipCloseFileInZip, err => %d\n", err);
        exit(1);
    }
        
    err = zipClose(zf, "Test MiniZip");
    if(err != ZIP_OK) {
        printf("Error in zipClose, err => %d\n", err);
        exit(1);
    }
    
    printf("ZIP file created, name => %s\n", zip_fname);
    
    /* unZip */
    printf("---------- Test unZIP ----------\n");
    
    unzFile unzf = unzOpen64(zip_fname);
    if (unzf == NULL) {
        printf("Error in unzOpen64, fname => %s\n", zip_fname);
        exit(1);
    }

    err = print_zip_info(unzf);
    if (err != UNZ_OK) {
        printf("Read ZIP info error, err => %d\n", err);
        exit(1);
    }
    
    err = unzGoToFirstFile(unzf);
    if (err != UNZ_OK) {
        printf("Error in unzGoToFirstFile, err => %d\n", err);
        exit(1);
    }
    
    unz_file_info64 unz_fi;    
    err = unzGetCurrentFileInfo64(unzf, &unz_fi, NULL, 0, NULL, 0, NULL, 0);
    if (err != UNZ_OK) {
        printf("Error in unzGetCurrentFileInfo64, err => %d\n", err);
        exit(1);
    }
    
    /* Compare size */
    if (unz_fi.uncompressed_size != (ZPOS64_T) SRC_SIZE) {
        printf("Error in Zip, failed comapre size. In Zip => %Ld, source size => %Ld\n", unz_fi.uncompressed_size, (ZPOS64_T) SRC_SIZE);
        exit(1);
    }
    
    err = unzOpenCurrentFile(unzf);
    if (err != UNZ_OK) {
        printf("Error in unzOpenCurrentFile, err => %d\n", err);
        exit(1);
    }
    
    char* read_data = malloc(SRC_SIZE);
    if (read_data == NULL) {
        printf("Can`t allocate read buffer\n");
        exit(1);
    }
    
    err = unzReadCurrentFile(unzf, read_data, SRC_SIZE);
    if (err < 0) {
        printf("Error in unzReadCurrentFile, err => %d\n", err);
        exit(1);
    }

    if (memcmp(src_data, read_data, SRC_SIZE) != 0) {
        printf("Error in zip, source and uncompressed data not equal.\n");
        exit(1);
    }

    err = unzClose(unzf);
    if (err != UNZ_OK) {
        printf("Error in unzClose, err => %d\n", err);
        exit(1);
    }
    
    free(src_data);
    free(read_data);
    return 0;
}

void init(void) {
    srand(time(0));
}

void fill_data(char* data, size_t len) {
    for (size_t i = 0; i < len; i++) {
        *(data + i) = (char) rand();
    }
}

int print_zip_info(unzFile unzf) {
    char comment[256] = {0};
    int err;
    err = unzGetGlobalComment(unzf, comment, sizeof(comment));
    if (err < 0) {
        printf("Error in unzGetGlobalComment, err => %d\n", err);
        return  err;
    }
    printf("unZIP. Global comment => %s\n", comment);
    
    err = unzGoToFirstFile(unzf);
    if (err != UNZ_OK) {
        printf("Error in unzGoToFirstFile, err => %d\n", err);
        return err;
    }
    
    unz_global_info64 gi;
    err = unzGetGlobalInfo64(unzf, &gi);
    if (err != UNZ_OK) {
        printf("Error in unzGetGlobalInfo64, err => %d\n", err);
        return err;
    }
    printf("  Length  Method     Size Ratio   Date    Time   CRC-32     Name\n");
    printf("  ------  ------     ---- -----   ----    ----   ------     ----\n");

    for (uLong i=0; i < gi.number_entry; i++) {
        unz_file_info64 file_info;    
        char fname_inzip[256];
        err = unzGetCurrentFileInfo64(unzf, &file_info, fname_inzip, sizeof(fname_inzip), NULL, 0, NULL, 0);
        if (err != UNZ_OK) {
            printf("Error in unzGetCurrentFileInfo64, err => %d\n", err);
            return err;
        }
        
        uLong ratio = 0;
        if (file_info.uncompressed_size>0) {
            ratio = (uLong)((file_info.compressed_size*100)/file_info.uncompressed_size);
        }
        
        char crypt = ' ';
        if ((file_info.flag & 1) != 0) {
            char crypt = '*';
        }
        
        const char* str_method = NULL;
        if (file_info.compression_method==0) {
            str_method = "Stored";
        } else if (file_info.compression_method == Z_DEFLATED) {
            uInt iLevel=(uInt)((file_info.flag & 0x6)/2);
            if (iLevel == 0) {
              str_method = "Defl:N";
            } else if (iLevel == 1) {
              str_method = "Defl:X";
            } else if ((iLevel == 2) || (iLevel == 3)) {
              str_method="Defl:F"; /* 2:fast , 3 : extra fast*/
            }
        } else if (file_info.compression_method==Z_BZIP2ED) {
              str_method="BZip2 ";
        } else {
            str_method="Unkn. ";
        }
        
        Display64BitsSize(file_info.uncompressed_size, 7);
        printf("  %6s%c", str_method, crypt);
        Display64BitsSize(file_info.compressed_size, 7);
        printf(" %3lu%%  %2.2lu-%2.2lu-%2.2lu  %2.2lu:%2.2lu  %8.8lx   %s\n",
                ratio,
                (uLong)file_info.tmu_date.tm_mon + 1,
                (uLong)file_info.tmu_date.tm_mday,
                (uLong)file_info.tmu_date.tm_year - 1900,
                (uLong)file_info.tmu_date.tm_hour,(uLong)file_info.tmu_date.tm_min,
                (uLong)file_info.crc,
                fname_inzip
        );
        if ((i+1) < gi.number_entry) {
            err = unzGoToNextFile(unzf);
            if (err!=UNZ_OK) {
                printf("Error in unzGoToNextFile, err => %d\n", err);
                return err;
            }
        }
    }
    
    return UNZ_OK;
}

void Display64BitsSize(ZPOS64_T n, int size_char)
{
    /* to avoid compatibility problem , we do here the conversion */
    char number[21];
    int offset = 19;
    int pos_string = 19;
    number[20]=0;
    for (;;) {
        number[offset] = (char)((n%10)+'0');
      if (number[offset] != '0') {
          pos_string = offset;
      }
      n /= 10;
      if (offset==0) {
          break;
      }
      offset--;
  }

  int size_display_string = 19-pos_string;
  while (size_char > size_display_string) {
          size_char--;
          printf(" ");
   }

  printf("%s",&number[pos_string]);
}

