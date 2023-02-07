from pytube import YouTube as pytube_youtube, StreamQuery
from typing import List, Union
import os


class YoutubeDownloader:
    MAX_ATTEMPT = 2
    WEBSITE_NAME = 'YouTube'
    

    def __init__(self, url: str, path_output: str, project_name: str) -> None:
        self.attempts = 0
        self.url_youtube = pytube_youtube(url)
        self.path_output_videos = os.path.join(path_output, "Videos", project_name, self.WEBSITE_NAME)
        self.path_output_audios = os.path.join(path_output, "Music", project_name, self.WEBSITE_NAME)


    def get_properties_by_url(self) -> None:
        """
        This method retrieves the properties of a YouTube video from a given URL. 
        It assigns the title, author, rating, length, publish date 
        and views of the video to corresponding attributes. 
        It also gets the available video and audio formats for the video and assigns 
        them to video_format and audio_format attributes, respectively. 
        The formats are sorted by resolution (for video) 
        and bit rate (for audio) in descending order.

        Returns: None
        """
        self.name_file = self.url_youtube.title
        self.author_file = self.url_youtube.author
        self.length_file = self.url_youtube.length
        self.publish_date_file = self.url_youtube.publish_date
        self.publish_date_file_formatted = self.publish_date_file.strftime('%d-%m-%Y')
        self.views_file = self.url_youtube.views

        self.video_format = list()
        self.audio_format = list()
        for stream in self.url_youtube.streams:
            if "video" in stream.mime_type and stream.resolution and stream.mime_type:
                if stream.abr:
                    self.video_format.append((stream.resolution, stream.mime_type, stream.fps, True, stream.filesize))
                else:
                    self.video_format.append((stream.resolution, stream.mime_type, stream.fps, False, stream.filesize))
            elif "audio" in stream.mime_type:
                self.audio_format.append((stream.abr, stream.mime_type, stream.filesize))
        self.video_format = sorted(self.video_format, key=lambda x: int(x[0].split("p")[0]), reverse=True)
        self.audio_format = sorted(self.audio_format, key=lambda x: int(x[0].split("kbps")[0]), reverse=True)

        
    def show_basic_properties(self) -> None:
        """
        This method prints out the basic properties of a YouTube video. 
        It displays the title, author, rating, length, publish date, and views of the video.

        Returns: None
        """
        print("\n -------- Basic Infos -------- ")
        print(" - Name:", self.name_file)
        print(" - Author:", self.author_file)
        minutes, seconds = divmod(self.length_file, 60)
        print(f" - Length: {minutes}:{seconds:02d}")
        print(" - Publish date:", self.publish_date_file_formatted)
        print(" - Views:", self.views_file)
        print(" ----------------------------- ")
        return None


    def select_video_or_audio(self) -> Union[int, None]:
        """
        This function allows the user to select a video or audio option from the available options.
        The options available are:
        - 0: both video and audio
        - 1: video only
        - 2: audio only

        Returns:
        Union[int, None]: An integer representing the chosen option, or None if no files were found.
        """
        print("\n - Choose files to download! -")
        if (self.video_format) and (self.audio_format):
            print(" - 0. Both Video and Audio")
            print(" - 1. Video file")
            print(" - 2. Audio file")            
            while True:
                try:
                    option = int(input(" - Select an option: "))
                    if option == 0:
                        return 0
                    elif option == 1:
                        return 1
                    elif option == 2:
                        return 2
                    else:
                        print(" - Invalid option, please try again.")
                except ValueError:
                    print(" - Invalid option, please enter a valid number.")
        else:
            if self.video_format:
                print(" - 1. Found only video file!")
                return 1
            elif self.audio_format:
                print(" - 2. Found only audio file!")
                return 2
            else:
                print(" - Files were not found! Check URL and come back soon!")
                return None


    def handle_format_file_selection(self, file: str, options: List[tuple]) -> tuple:
        """
        Prompts the user to select the format file of a video or audio from a list of options.

        Args:
        - file (str): The type of the file to be selected, either "Video" or "Audio".
        - options (List[tuple]): A list of tuples containing the options of format files to be selected.

        Returns:
        - tuple: The selected format file tuple, with the first element being the quality and the second element being the type.

        Raises:
        - ValueError: If the user inputs an invalid option.

        """
        print(f"\n - {file} Format file menu -")
        
        for index, format_file in enumerate(options):
            if file == "Video":
                print(fr" - {str(index).rjust(2)} - Resolution: {format_file[0].rjust(7)} - Type: {str(format_file[1]).rjust(10)} - FPS: {str(format_file[2]).rjust(3)} - Has Audio: {str(format_file[3]).rjust(5)} - Filesize: {format_file[4] / 10**6:.02f}Mb")
            elif file == "Audio":
                print(fr" - {str(index).rjust(2)} - Bitrate: {format_file[0].rjust(7)} - Type: {str(format_file[1]).rjust(10)} - Filesize: {format_file[2] / 10**6:.02f}Mb")
        while True:
            try:
                selected = int(input(" - Select an option: "))
                if selected not in range(len(options)):
                    raise ValueError
                break
            except ValueError:
                print(" - Invalid option, please enter a valid integer that corresponds to the options above.")
        format_file_user = options[selected]
        print(f" - {format_file_user[0]}, {format_file_user[1]} has been selected!")
        return format_file_user


    def check_available(self, file: str, selected_format: tuple) -> Union[StreamQuery, None]:
        """
        Check if the selected file format is available to be downloaded.

        Args:
        - file (str): The type of file being checked ("Video", "Audio").
        - selected_format (tuple): The format quality and type to be checked for availability.
        
        Returns:
        StreamQuery or None: The StreamQuery object representing the available format if found, else None.
        """
        quality = selected_format[0]
        type_file = selected_format[1]
        try:
            if file == "Video":
                streams = self.url_youtube.streams.filter(resolution=quality, mime_type=type_file, only_audio=False).first()
            elif file == "Audio":
                streams = self.url_youtube.streams.filter(abr=quality, mime_type=type_file, only_audio=False).first()
        except Exception as e:
            raise e
        else:
            if streams:
                print(f' - {quality}, {type_file} is available to download!')
                return streams
            else:
                print(f' - {quality}, {type_file} is not available')
                return None


    def request_and_make_download(self, file: str, format_files: List[tuple], path_output: str) -> None:
        """
        This function handles the file format selection, checks if it's available to download,
        and tries to download the selected file. If the download fails, it retries up to `MAX_ATTEMPT` times.
        
        Args:
        - file: a string that indicates which file is being processed, either "Video" or "Audio".
        - format_files: a list of tuples containing the available file formats to download.
        - path_output: a string with the path to the output folder.
        
        Returns: None
        """
        self.selected_format = self.handle_format_file_selection(file, format_files)
        self.stream = self.check_available(file, self.selected_format)
        if self.stream is None:
            print(f" - {file} Download failed, try again.")
            self.attempts += 1
            if self.attempts < self.MAX_ATTEMPT:
                self.request_and_make_download(file, format_files, path_output)
            else:
                print(" - Maximum count of attempts reached, ending process.")
        else:
            self.stream.download(path_output)
            path_file_output = fr"{path_output}\\{self.name_file}"
            print(f" - {file} Downloaded successfully to {path_file_output}")
        return None


    def check_option_and_try_download(self, option_video_audio: Union[int, None]) -> None:
        """
        This function presents the options to the user to select if they want to download video, audio or both.
        If the user selects the option 0 - both, the function will check and make the download of both video and audio.
        If the user selects the option 1 - video, the function will check and make the download of video only.
        If the user selects the option 2 - audio, the function will check and make the download of audio only.
        If the user selects any other option, the function will return None.

        :param option_video_audio: (int) option selected by the user to download video, audio or both.
        :return: None
        """ 
        if option_video_audio in [0, 1]:
            self.request_and_make_download(file="Video", format_files=self.video_format, path_output=self.path_output_videos)
        if option_video_audio in [0, 2]:
            self.request_and_make_download(file="Audio", format_files=self.audio_format, path_output=self.path_output_audios)
        return None


    def run(self) -> None:
        self.get_properties_by_url()
        self.show_basic_properties()
        option_video_audio = self.select_video_or_audio()
        if option_video_audio is None:
            return None
        return self.check_option_and_try_download(option_video_audio)