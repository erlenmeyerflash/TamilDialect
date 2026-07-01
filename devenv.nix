{ pkgs, lib, config, inputs, ... }:

{
  packages = with pkgs; [
    git
  ];

  languages.python = {
    enable = true;
    version = "3.11";
    venv.enable = true;
    venv.requirements = ''
      openai-whisper
      yt-dlp
      nltk

      transformers
      datasets
      torch
      pandas
      numpy
      scipy
      scikit-learn
      jupyter
    '';
  };
}
