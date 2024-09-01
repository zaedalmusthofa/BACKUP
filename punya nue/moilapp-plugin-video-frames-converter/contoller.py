from src.plugin_interface import PluginInterface
from src.models.moilutils import MoilUtils
from PyQt6.QtWidgets import QWidget
from PyQt6 import QtCore, QtGui, QtWidgets
from .model_main import Model
from .ui_main import Ui_Form

import os, sys, shutil, cv2, numpy, math
import subprocess
from glob import glob
from pathlib import Path
from getpass import getpass
from time import time, sleep
from random import randrange, shuffle

class Controller(QWidget):
    def __init__(self, model=Model):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.model = model
        
        self.supported_video_formats = ["MP4", "AVI", "MOV", "WMV", "MKV", "FLV", "MPEG", "3GP"]
        self.multiplier_estimations = [3, 2, 4, 3, 8, 3, 2, 2]
        self.default_path = f"{str(Path(__file__).parent.resolve())}"
        self.saved_frames_path = f"{self.default_path}\\saves"
        self.uploaded_video_file_format = ""
        
        self.video_logger_texts_list, self.frames_logger_texts_list = [], []
        self.display_video_logger_text, self.display_frames_logger_text = "", ""
        
        self.count_captured_frames = 0
        self.completed_percentage = 0
        
        self.video_path, self.video = None, None
        self.thumbnail, self.frames = None, None
        self.cancel_conversion_process = False
        self.render_video = False
        
        self.set_stylesheet()
    
    def set_stylesheet(self):
        self.ui.VideoLabelOutput.setStyleSheet(self.model.style_label())
        self.ui.FramesLabelOutput.setStyleSheet(self.model.style_label())
        self.ui.FPSLabel.setStyleSheet(self.set_custom_font_style("Fira Code Medium", 11))
        
        self.ui.UploadVideoButton.clicked.connect(self.upload_video)
        self.ui.ConvertButton.clicked.connect(self.vtf_convert)
        self.ui.CancelButton.clicked.connect(self.abort_conversion_process)
        self.ui.ClearVideoButton.clicked.connect(self.clear_video)
    
    def set_custom_font_style(self, font_family, font_size):
        stylesheet = f"""
            font: {font_size}pt "{font_family}";
        """
        return stylesheet
    
    def vtf_show_image_to_label(self, label, image, width, height, angle=0, plusIcon=False, scale_content=False):
        if scale_content is True:
            label.setScaledContents(True)

        else:
            label.setScaledContents(False)
            image = MoilUtils.resize_image(image, width)
            label.setMinimumSize(QtCore.QSize(width, height))
            label.setMaximumSize(QtCore.QSize(width, height))

        image = MoilUtils.rotate_image(image, angle)
        if plusIcon:
            # draw plus icons on image and show to label
            h, w = image.shape[:2]
            w1 = round((w / 2) - 10)
            h1 = round(h / 2)
            w2 = round((w / 2) + 10)
            h2 = round(h / 2)
            w3 = round(w / 2)
            h3 = round((h / 2) - 10)
            w4 = round(w / 2)
            h4 = round((h / 2)) + 10
            MoilUtils.draw_line(image, (w1, h1), (w2, h2))
            MoilUtils.draw_line(image, (w3, h3), (w4, h4))

        image = QtGui.QImage(image.data, image.shape[1], image.shape[0], QtGui.QImage.Format.Format_RGB888).rgbSwapped()
        label.setPixmap(QtGui.QPixmap.fromImage(image))
        
    def create_directory(self, source_path: str) -> None:
        try:
            if (not os.path.exists(source_path)): os.makedirs(source_path)
            else:
                shutil.rmtree(source_path)
                os.makedirs(source_path)
        except OSError:
            print(f"[FAIL] ERROR: Unable to create a (new) directory with name '{source_path}'!")
            sys.exit(1)
        return None

    def calculate_percentage(self, IntegerValue: int) -> list[int]:
        SumOfIndividuals: list[int] = []
        Individuals: int = 0
        Remainder: int   = 0
        
        if (IntegerValue >= 100):
            Individuals = IntegerValue // 100
            Remainder   = IntegerValue % 100
            
            for _ in range(Remainder): SumOfIndividuals.append(Individuals + 1)
            for _ in range(100 - Remainder): SumOfIndividuals.append(Individuals)
            shuffle(SumOfIndividuals)
            for Index in range(1, len(SumOfIndividuals)):
                if (Index != len(SumOfIndividuals)): SumOfIndividuals[Index] = SumOfIndividuals[Index] + SumOfIndividuals[Index - 1]
        
        elif (0 <= IntegerValue < 100):
            TempIntegerValue: int = IntegerValue + (math.ceil(100 / (IntegerValue / 0.5)))
            Individuals = TempIntegerValue // 100
            Remainder   = TempIntegerValue % 100
            
            for _ in range(Remainder): SumOfIndividuals.append(Individuals + 1)
            for _ in range(100 - Remainder): SumOfIndividuals.append(Individuals)
            shuffle(SumOfIndividuals)
            for Index in range(1, len(SumOfIndividuals)):
                if (Index != len(SumOfIndividuals)): SumOfIndividuals[Index] = SumOfIndividuals[Index] + SumOfIndividuals[Index - 1]
        
        else:
            print(f"[FAIL] ERROR: Unable to process 'calculate_percentage()' with 'IntegerValue' being negative!")
            sys.exit(1)
            
        return SumOfIndividuals
    
    def convert_video_into_frames(self, VideoSourcePath: str, SaveInDirectory: str, PerFrameCapture: int, EstimatedTotalFrames: int, *, ImageFormat: str = "PNG", ImageFileName: str = "IMAGE"):
        SaveInPath = f"{SaveInDirectory}/{VideoSourcePath.split('/')[-1].strip().partition('.')[0].strip()}"
        self.create_directory(SaveInPath)

        # 'CumulativePercentageByFrames' were used to calculate each chunks of 1% while
        # completing the process, and monitored by the 'completed_percentage'.
        CumulativePercentageByFrames: list[int] = self.calculate_percentage(EstimatedTotalFrames)
        self.count_captured_frames: int = 0
        self.completed_percentage: int = 0
        self.ui.ProgressBar.setValue(0)

        start = time()
        while True and not self.cancel_conversion_process:
            ReturnValue, Frames = self.video.read()

            if (ReturnValue == False):
                self.video = cv2.VideoCapture(self.video_path)
                self.frames_logger_texts_list.insert(0, f"[INFO] Successfully converting {int(self.count_captured_frames // int(PerFrameCapture))} frames from the given video file!\n")
                self.frames_logger_texts_list.insert(1, f"[INFO] Conversion process took {time() - start:.3f} seconds.\n\n")
                self.frames_logger_texts_list.insert(2, f"[INFO] Task Completed: ({int(self.count_captured_frames // int(PerFrameCapture))} / {EstimatedTotalFrames})\n... {'/'.join(SaveInPath.split('/')[-2:])}/{ImageFileName}_{int(self.count_captured_frames // int(PerFrameCapture))}.{ImageFormat.lower()} has been saved.\n")
                self.display_frames_logger_text = self.display_frames_logger_text.join(self.frames_logger_texts_list)
                self.ui.FramesConversionLoggerText.setText(self.display_frames_logger_text)
                self.frames_logger_texts_list.clear()
                self.display_thumbnail()
                break

            if (self.count_captured_frames == 0):
                cv2.imwrite(f"{SaveInPath}\\{ImageFileName}_0.{ImageFormat.lower()}", Frames)
                self.ui.FramesConversionLoggerText.setText(f"[INFO] Task Completed: ({int(self.count_captured_frames // int(PerFrameCapture))} / {EstimatedTotalFrames})\n... {'/'.join(SaveInPath.split('/')[-2:])}/{ImageFileName}_0.{ImageFormat.lower()} has been saved.\n")
                
                self.count_captured_frames += 1
                self.completed_percentage += 1
            else:
                if (self.count_captured_frames % int(PerFrameCapture) == 0):
                    cv2.imwrite(f"{SaveInPath}\\{ImageFileName}_{int(self.count_captured_frames // int(PerFrameCapture))}.{ImageFormat.lower()}", Frames)
                    self.ui.FramesConversionLoggerText.setText(f"[INFO] Task Completed: ({int(self.count_captured_frames // int(PerFrameCapture))} / {EstimatedTotalFrames})\n... {'/'.join(SaveInPath.split('/')[-2:])}/{ImageFileName}_{int(self.count_captured_frames // int(PerFrameCapture))}.{ImageFormat.lower()} has been saved.\n")
                    
                    for Index in range(len(CumulativePercentageByFrames)):
                        if (int(self.count_captured_frames // int(PerFrameCapture)) == CumulativePercentageByFrames[Index] and self.completed_percentage <= 100):
                            self.completed_percentage += 1

            if self.count_captured_frames % PerFrameCapture == 0:
                self.frames_original = cv2.imread(f"{SaveInPath}\\{ImageFileName}_{int(self.count_captured_frames // int(PerFrameCapture))}.{ImageFormat.lower()}")
                self.frames = self.frames_original.copy()
                self.vtf_show_image_to_label(self.ui.FramesLabelOutput, self.frames, 716, 411)
                            
            self.count_captured_frames += 1
            self.ui.ProgressBar.setValue(self.completed_percentage)
        self.ui.ProgressBar.setValue(100)
    
    def upload_video(self):
        if self.render_video: self.ui.VideoLoggerText.setText(f"[WARNING] You can ONLY upload ONE video at a time!\n[NOTE] Make sure you clear the uploaded video first and then proceed to upload any video again... .\n\n{self.display_video_logger_text}"); return
        self.create_directory(f"{self.default_path}\\cache")
            
        file = self.model.select_file()
        self.uploaded_video_file_format = file.partition('/')[-1].strip().split('.')[-1].split('.')[-1].upper()
        if self.uploaded_video_file_format not in self.supported_video_formats: self.ui.VideoLoggerText.setText(f"[ERROR] Failed to upload video file named:\n    ... \"{file.partition('/')[-1].strip()}\"!\n[NOTE] Make sure upload the CORRECT format for file videos.\n[INFO] Here are the 8 SUPPORTED video file formats:\n   ... {', '.join(self.supported_video_formats)}.\n\n{self.display_video_logger_text}"); return
        if file:
            if file:
                self.moildev = self.model.connect_to_moildev(parameter_name=file)
            video_input_path = file
            image_output_path = f"{self.default_path}/cache/thumbnail.png"
            
            try:
                subprocess.call(['ffmpeg', '-i', video_input_path, '-ss', '00:00:03.000', '-vframes', '1', image_output_path])
            except FileNotFoundError:
                self.ui.VideoLoggerText.setText("[ERROR] \"ffmpeg\" failed to generate the thumbnail for the uploaded video!\n[INFO] Please install the \"ffmpeg\" application (or binary files) first on their website, with the link below:\n\n  ... https://ffmpeg.org/download.html")
                return
            
            self.thumbnail_original = cv2.imread(image_output_path)
            self.thumbnail = self.thumbnail_original.copy()
            self.render_video = True
            
            self.video_path = file
            self.video = cv2.VideoCapture(self.video_path)
            self.display_thumbnail()
    
    def clear_video(self):
        self.uploaded_video_file_format = ""
    
        self.video_logger_texts_list, self.frames_logger_texts_list = [], []
        self.display_video_logger_text, self.display_frames_logger_text = "", ""
        
        self.estimated_total_frames = 0
        self.count_captured_frames: int = 0
        self.completed_percentage: int = 0
        
        self.video_path, self.video = None, None
        self.thumbnail, self.frames = None, None
        self.cancel_conversion_process = False
        self.render_video = False
        
        self.ui.VideoLabelOutput.clear()
        self.ui.FramesLabelOutput.clear()
        
        self.ui.VideoLoggerText.setText("")
        self.ui.FramesConversionLoggerText.setText("")
        self.ui.ProgressBar.setValue(0)
        
            # os.remove(f"{self.default_path}/cache/thumbnail.jpg")
    
    def abort_conversion_process(self):
        self.cancel_conversion_process = True

    def display_thumbnail(self):
        self.already_delete = False
        # self.ui.FramesConversionLoggerText.setText("")
        
        self.vtf_show_image_to_label(self.ui.VideoLabelOutput, self.thumbnail, 716, 411)
        
        __RANDOMIZED_FPS_LIST: list[float] = [1.00, 5.00, 10.00, 15.00, 20.00, 23.98, 24.00, 25.00, 29.97, 30.00, 40.00, 50.00, 59.94, 60.00, 75.00, 120.00, 144.00, 165.00, 240.00, 360.00, 480.00]
        # __RANDOMIZED_SEC: int   = randrange(1, (pow(2, 10) + 1))
        # __RANDOMIZED_PFC: int   = randrange(10, (__RANDOMIZED_SEC // randrange(1, 6)))
        shuffle(__RANDOMIZED_FPS_LIST)
        # __RANDOMIZED_FPS: float = __RANDOMIZED_FPS_LIST[randrange(0, len(__RANDOMIZED_FPS_LIST))]
        
        total_estimation_time = round(float(f"{randrange(0, self.multiplier_estimations[self.supported_video_formats.index(self.uploaded_video_file_format)])}.{randrange(1, 10)}{randrange(1, 10)}{randrange(1, 10)}"), 3)
        estimation_time_multiplier = round(os.path.getsize(self.video_path) / 1_000_000, 3)

        video_frame_rate = self.video.get(cv2.CAP_PROP_FPS)
        video_duration = round((self.video.get(cv2.CAP_PROP_FRAME_COUNT)) / video_frame_rate, 2)
        video_frame_by_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_frame_by_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_resolution = int(video_frame_by_height)
        estimated_total_frames = int((video_frame_rate * video_duration) / self.ui.FPSSpinBox.value())
        
        self.video_logger_texts_list.append(f"[INFO] Getting the video file path...\n")
        self.video_logger_texts_list.append(f"[INFO]     Video file path: {self.video_path}\n")
        self.video_logger_texts_list.append(f"[INFO] Reading the video file...\n")
        self.video_logger_texts_list.append(f"[INFO]     Video file name:  {self.video_path.split('/')[-1].partition('.')[0].strip()}\n")
        self.video_logger_texts_list.append(f"[INFO]     Video format:     {self.video_path.split('/')[-1].partition('.')[-1].strip().upper()}\n")
        self.video_logger_texts_list.append(f"[INFO]     Video frame rate: {round(video_frame_rate, 2):.2f} FPS\n")
        self.video_logger_texts_list.append(f"[INFO]     Video duration:   {round(video_duration, 2):.2f} seconds\n")
        self.video_logger_texts_list.append(f"[INFO]     Video resolution: {video_resolution}p ({video_frame_by_width}x{video_frame_by_height})\n")
        self.video_logger_texts_list.append(f"[INFO]     File size:        {round(os.path.getsize(self.video_path) / 1_000_000, 3)} MB ({os.path.getsize(self.video_path)} in bytes)\n")
        
        self.video_logger_texts_list.append(f"[INFO] Estimated total converted frames:  {estimated_total_frames} frames.\n")
        self.video_logger_texts_list.append(f"[INFO] Estimated conversion time process: {round(estimation_time_multiplier * total_estimation_time, 3)} seconds.\n")
        self.video_logger_texts_list.append(f"   ... (estimation time could be better, or worse, depending on your computer)\n")
        self.video_logger_texts_list.append(f"   ... (other factors come from the video's resolution, format file, estimated total frames, etc.)\n")
        
        self.display_video_logger_text = ""
        self.display_video_logger_text = self.display_video_logger_text.join(self.video_logger_texts_list)
        self.ui.VideoLoggerText.setText(self.display_video_logger_text)
    
    def vtf_convert(self):
        if not self.render_video: self.ui.FramesConversionLoggerText.setText("[ERROR] No uploaded video file to be found!\n    ... Please upload a single video file first (with the listed of supported formats) before doing some conversion process... ."); return
        
        self.video_logger_texts_list.insert(0, f"[INFO] Proceed with VIDEO to FRAME(s) conversion. Please wait... .\n")
        self.video_logger_texts_list.insert(1, f"[INFO] Converting file video from: {self.video_path.split('/')[-1].strip()}\n")
        self.video_logger_texts_list.insert(2, f"[NOTE] Conversion process can be longer than estimated time, since\n")
        self.video_logger_texts_list.insert(3, f"       the conversion process took CPU/GPU graphical processing... .\n\n")
        
        self.video_logger_texts_list.insert(4, f"[INFO] Results will be saved in the following path:\n")
        self.video_logger_texts_list.insert(5, f"[INFO]     Saved in: {self.saved_frames_path}\\{self.video_path.split('/')[-1].strip()[:-4]}\\...\n")
        
        self.display_video_logger_text = ""
        self.display_video_logger_text = self.display_video_logger_text.join(self.video_logger_texts_list)
        self.ui.VideoLoggerText.setText(self.display_video_logger_text)
        self.video_logger_texts_list.clear()
        
        per_frame_capture = self.ui.FPSSpinBox.value()
        video_frame_rate = self.video.get(cv2.CAP_PROP_FPS)
        video_duration = round((self.video.get(cv2.CAP_PROP_FRAME_COUNT)) / video_frame_rate, 2)
        estimated_total_frames = int((video_frame_rate * video_duration) / per_frame_capture)
        
        self.convert_video_into_frames(self.video_path, self.saved_frames_path, per_frame_capture, estimated_total_frames)
        
class VideoFramesConverter(PluginInterface):
    def __init__(self):
        super().__init__()
        self.widget = None
        self.description = "Moilapp Plugin: Video to Sequence of Frames Converter"

    def set_plugin_widget(self, model):
        self.widget = Controller(model)
        return self.widget

    def set_icon_apps(self):
        return "vtf-icon.png"

    def change_stylesheet(self):
        self.widget.set_stylesheet()
