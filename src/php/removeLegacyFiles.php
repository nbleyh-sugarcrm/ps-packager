<?php

if (isset($this->installdefs['remove_files'])) {
    foreach($this->installdefs['remove_files'] as $relpath){
        if (is_dir($relpath)) {
            rmdir_recursive($relpath);
        } else {
            unlink($relpath);
        }
    }
}

?>