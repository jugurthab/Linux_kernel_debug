#undef TRACEPOINT_PROVIDER
 
#define TRACEPOINT_PROVIDER smile_directory_explorer_lttng_provider

#undef TRACEPOINT_INCLUDE
#define TRACEPOINT_INCLUDE "./directory-explorer-tracepoint.h"

#if !defined(_DIRECTORY_EXPLORER_TRACEPOINT) || defined(TRACEPOINT_HEADER_MULTI_READ)
#define _DIRECTORY_EXPLORER_TRACEPOINT

#include <lttng/tracepoint.h>

TRACEPOINT_EVENT(
    smile_directory_explorer_lttng_provider, //provider name defined above with TRACEPOINT_PROVIDER
    smile_first_tracepoint, // Tracepoint name
    TP_ARGS(
        int, smile_file_number,
        char*, smile_file_name
    ),
    TP_FIELDS(
        ctf_integer(int, smile_file_number_label, smile_file_number)
        ctf_string(smile_file_name_label, smile_file_name)        
    )
)

#endif /* _DIRECTORY_EXPLORER_TRACEPOINT */

#include <lttng/tracepoint-event.h>

