# https://stackoverflow.com/questions/56494070/how-to-use-pdfminer-six-with-python-3

class PdfReader:

    def __init__(self):
        pass

    def test(self, file):
        from pdfminer3.layout import LAParams, LTTextBox
        from pdfminer3.pdfpage import PDFPage
        from pdfminer3.pdfinterp import PDFResourceManager
        from pdfminer3.pdfinterp import PDFPageInterpreter
        from pdfminer3.converter import PDFPageAggregator
        from pdfminer3.converter import TextConverter
        import io

        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        print("FILE", file)
        with open(file, 'rb') as fh:
            for i, page in enumerate(PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True)):
                page_interpreter.process_page(page)
                print("===================",i,"=================")

            text = fake_file_handle.getvalue()

        # close open handles
        converter.close()
        fake_file_handle.close()

        print(text)

        """
        > pdf2txt.py [-P password] [-o output] [-t text|html|xml|tag]
             [-O output_dir] [-c encoding] [-s scale] [-R rotation]
             [-Y normal|loose|exact] [-p pagenos] [-m maxpages]
             [-S] [-C] [-n] [-A] [-V]
             [-M char_margin] [-L line_margin] [-W word_margin]
             [-F boxes_flow] [-d]
             input.pdf ...
-P password : PDF password.
-o output : Output file name.
-t text|html|xml|tag : Output type. (default: automatically inferred from the output file name.)
-O output_dir : Output directory for extracted images.
-c encoding : Output encoding. (default: utf-8)
-s scale : Output scale.
-R rotation : Rotates the page in degree.
-Y normal|loose|exact : Specifies the layout mode. (only for HTML output.)
-p pagenos : Processes certain pages only.
-m maxpages : Limits the number of maximum pages to process.
-S : Strips control characters.
-C : Disables resource caching.
-n : Disables layout analysis.
-A : Applies layout analysis for all texts including figures.
-V : Automatically detects vertical writing.
-M char_margin : Speficies the char margin.
-W word_margin : Speficies the word margin.
-L line_margin : Speficies the line margin.
-F boxes_flow : Speficies the box flow ratio.
-d : Turns on Debug output.

        """

def main():
    pdfReader = PdfReader()
    pdfReader.test("/Users/pm286/projects/openDiagram/physchem/liion/PMC7040616/fulltext.pdf");

if __name__ == "__main__":
    main()
