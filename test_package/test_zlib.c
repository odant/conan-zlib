#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <zlib.h>

const char text[] = ""
"Marianne or husbands if at stronger ye. Considered is as middletons uncommonly. Promotion perfectly ye consisted so. His chatty dining for effect ladies active. Equally journey wishing not several behaved chapter she two sir. Deficient procuring favourite extensive you two. Yet diminution she impossible understood age.\n"
"\n"
"Must you with him from him her were more. In eldest be it result should remark vanity square. Unpleasant especially assistance sufficient he comparison so inquietude. Branch one shy edward stairs turned has law wonder horses. Devonshire invitation discovered out indulgence the excellence preference. Objection estimable discourse procuring he he remaining on distrusts. Simplicity affronting inquietude for now sympathize age. She meant new their sex could defer child. An lose at quit to life do dull.\n"
"\n"
"Of on affixed civilly moments promise explain fertile in. Assurance advantage belonging happiness departure so of. Now improving and one sincerity intention allowance commanded not. Oh an am frankness be necessary earnestly advantage estimable extensive. Five he wife gone ye. Mrs suffering sportsmen earnestly any. In am do giving to afford parish settle easily garret.\n"
"\n"
"When be draw drew ye. Defective in do recommend suffering. House it seven in spoil tiled court. Sister others marked fat missed did out use. Alteration possession dispatched collecting instrument travelling he or on. Snug give made at spot or late that mr.\n"
"\n"
"Of recommend residence education be on difficult repulsive offending. Judge views had mirth table seems great him for her. Alone all happy asked begin fully stand own get. Excuse ye seeing result of we. See scale dried songs old may not. Promotion did disposing you household any instantly. Hills we do under times at first short an.\n"
"\n"
"Offices parties lasting outward nothing age few resolve. Impression to discretion understood to we interested he excellence. Him remarkably use projection collecting. Going about eat forty world has round miles. Attention affection at my preferred offending shameless me if agreeable. Life lain held calm and true neat she. Much feet each so went no from. Truth began maids linen an mr to after.\n"
"\n"
"Surrounded affronting favourable no mr. Lain knew like half she yet joy. Be than dull as seen very shot. Attachment ye so am travelling estimating projecting is. Off fat address attacks his besides. Suitable settling mr attended no doubtful feelings. Any over for say bore such sold five but hung.\n"
"\n"
"Lose eyes get fat shew. Winter can indeed letter oppose way change tended now. So is improve my charmed picture exposed adapted demands. Received had end produced prepared diverted strictly off man branched. Known ye money so large decay voice there to. Preserved be mr cordially incommode as an. He doors quick child an point at. Had share vexed front least style off why him.\n"
"\n"
"There worse by an of miles civil. Manner before lively wholly am mr indeed expect. Among every merry his yet has her. You mistress get dashwood children off. Met whose marry under the merit. In it do continual consulted no listening. Devonshire sir sex motionless travelling six themselves. So colonel as greatly shewing herself observe ashamed. Demands minutes regular ye to detract is.\n"
"\n"
"Concerns greatest margaret him absolute entrance nay. Door neat week do find past he. Be no surprise he honoured indulged. Unpacked endeavor six steepest had husbands her. Painted no or affixed it so civilly. Exposed neither pressed so cottage as proceed at offices. Nay they gone sir game four. Favourable pianoforte oh motionless excellence of astonished we principles. Warrant present garrets limited cordial in inquiry to. Supported me sweetness behaviour shameless excellent so arranging.\n"
"";

int main(int argc, char** argv) {
    printf("ZLIB version: %s\n", zlibVersion());
    printf("Original size: %zu bytes\n", sizeof(text));
    
    const uLong compress_buffer_size = compressBound(sizeof(text));
    printf("Required size buffer for compress: %lu\n", compress_buffer_size);
    char* compress_buffer = calloc(1, compress_buffer_size);
    if (compress_buffer == NULL) {
        printf("Error. Allocate compress_buffer failed.\n");
        exit(EXIT_FAILURE);
    }
    
    uLongf compressed_size = compress_buffer_size;
    int res = compress(compress_buffer, &compressed_size, text, sizeof(text));
    if (res != Z_OK) {
        printf("Error. Compress failed. Code: %d Message: %s\n", res, zError(res));
        exit(EXIT_FAILURE);
    }
    printf("Compressed size: %lu bytes\n", compressed_size);
    
    char* uncompress_buffer = calloc(1, sizeof(text));
    if (uncompress_buffer == NULL) {
        printf("Error. Allocate uncompress_buffer failed\n");
        exit(EXIT_FAILURE);
    }
    
    uLongf uncompressed_size = sizeof(text);
    res = uncompress(uncompress_buffer, &uncompressed_size, compress_buffer, compressed_size);
    if (res != Z_OK) {
        printf("Error. Uncompress failed. Code: %d Message: %s\n", res, zError(res));
        exit(EXIT_FAILURE);
    }
    
    if (uncompressed_size != sizeof(text)) {
        printf("Error. Invalid uncompress. Original size: %zu bytes, uncompressed size: %lu bytes\n", sizeof(text), uncompressed_size);
        exit(EXIT_FAILURE);
    } else if (memcmp(text, uncompress_buffer, sizeof(text)) != 0) {
        printf("Error. Invalid uncompress. Original and uncompressed data not equal.\n");
        exit(EXIT_FAILURE);
    }
    
    printf("Compress / uncompress OK\n");

    free(compress_buffer);
    free(uncompress_buffer);
    
    return EXIT_SUCCESS;
}
