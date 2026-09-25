import {Paperclip} from "lucide-react";



function FileUploadButton({ handleFileUpload , accept =  ".pdf,.doc,.docx,.txt", inputRef, disabled }) {


    return (
        <label className="icon-button">
            <Paperclip size={21} />
            <input
                type="file"
                accept={accept}
                onChange={handleFileUpload}
                className="hidden"
                ref={inputRef}
                disabled={disabled}
            />
        </label>
    )
}


export default FileUploadButton;