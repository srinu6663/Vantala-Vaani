import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Progress } from "@/components/ui/progress";
import { useNotification } from "@/components/notification";
import { uploadRecord, uploadChunk } from "@/lib/api";
import { insertContributionSchema } from "@shared/schema";
import { FileText, Mic, Video, Images, Upload, ArrowLeft, CloudUpload } from "lucide-react";
import { z } from "zod";

type UploadType = 'text' | 'audio' | 'video' | 'image';

interface UploadModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  userId: string;
}

const uploadFormSchema = insertContributionSchema.extend({
  file: z.instanceof(File).optional(),
});

type UploadFormData = z.infer<typeof uploadFormSchema>;

export function UploadModal({ open, onOpenChange, userId }: UploadModalProps) {
  const [selectedType, setSelectedType] = useState<UploadType | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const { showNotification } = useNotification();
  const queryClient = useQueryClient();

  const form = useForm<UploadFormData>({
    resolver: zodResolver(uploadFormSchema),
    defaultValues: {
      title: "",
      type: "",
      content: "",
      category: "",
      language: "",
      description: "",
      tags: [],
    },
  });

  const uploadMutation = useMutation({
    mutationFn: ({ formData, isChunked }: { formData: FormData; isChunked: boolean }) => {
      return isChunked ? uploadChunk(formData) : uploadRecord(formData);
    },
    onSuccess: () => {
      showNotification('Success', 'Content uploaded successfully!', 'success');
      queryClient.invalidateQueries({ queryKey: ['/api/v1/users', userId, 'contributions'] });
      resetModal();
    },
    onError: (error: any) => {
      showNotification('Error', error.message || 'Upload failed', 'error');
      setIsUploading(false);
      setUploadProgress(0);
    },
  });

  const resetModal = () => {
    setSelectedType(null);
    setUploadProgress(0);
    setIsUploading(false);
    form.reset();
    onOpenChange(false);
  };

  const onSubmit = async (data: UploadFormData) => {
    setIsUploading(true);
    
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        return prev + Math.random() * 15;
      });
    }, 200);

    const formData = new FormData();
    formData.append('title', data.title);
    formData.append('type', selectedType!);
    formData.append('category', data.category || '');
    formData.append('language', data.language || '');
    formData.append('description', data.description || '');
    
    if (data.tags) {
      formData.append('tags', Array.isArray(data.tags) ? data.tags.join(',') : data.tags);
    }

    if (data.content) {
      formData.append('content', data.content);
    }

    if (data.file) {
      formData.append('file', data.file);
    }

    const isChunked = selectedType === 'audio' || selectedType === 'video';
    
    uploadMutation.mutate({ formData, isChunked });
  };

  const uploadTypes = [
    {
      key: 'text' as const,
      title: 'Text Content',
      description: 'Articles, stories, translations',
      icon: FileText,
      color: 'text-primary',
      bgColor: 'bg-primary/10 group-hover:bg-primary/20',
      borderColor: 'hover:border-primary hover:bg-primary/5',
    },
    {
      key: 'audio' as const,
      title: 'Audio Recording',
      description: 'Voice, music, pronunciation',
      icon: Mic,
      color: 'text-secondary',
      bgColor: 'bg-secondary/10 group-hover:bg-secondary/20',
      borderColor: 'hover:border-secondary hover:bg-secondary/5',
    },
    {
      key: 'video' as const,
      title: 'Video Content',
      description: 'Documentaries, tutorials, interviews',
      icon: Video,
      color: 'text-accent-foreground',
      bgColor: 'bg-accent group-hover:bg-accent/20',
      borderColor: 'hover:border-accent hover:bg-accent/5',
    },
    {
      key: 'image' as const,
      title: 'Images',
      description: 'Photos, artwork, documents',
      icon: Images,
      color: 'text-muted-foreground',
      bgColor: 'bg-muted group-hover:bg-muted/20',
      borderColor: 'hover:border-muted hover:bg-muted/5',
    },
  ];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        {!selectedType ? (
          // Type Selection
          <>
            <DialogHeader>
              <DialogTitle className="text-2xl font-bold">New Contribution</DialogTitle>
              <p className="text-muted-foreground">Choose the type of content you want to contribute</p>
            </DialogHeader>
            
            <div className="grid grid-cols-2 gap-4 py-4">
              {uploadTypes.map((type) => (
                <Button
                  key={type.key}
                  variant="outline"
                  className={`p-6 h-auto flex-col space-y-3 group ${type.borderColor} transition-all`}
                  onClick={() => {
                    setSelectedType(type.key);
                    form.setValue('type', type.key);
                  }}
                  data-testid={`upload-type-${type.key}`}
                >
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center ${type.bgColor}`}>
                    <type.icon className={`${type.color} text-xl h-6 w-6`} />
                  </div>
                  <div className="text-center">
                    <h3 className="font-medium text-card-foreground">{type.title}</h3>
                    <p className="text-sm text-muted-foreground mt-1">{type.description}</p>
                  </div>
                </Button>
              ))}
            </div>
          </>
        ) : (
          // Upload Form
          <>
            <DialogHeader className="flex flex-row items-center space-y-0 space-x-4">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSelectedType(null)}
                data-testid="button-back"
                className="text-muted-foreground hover:text-foreground"
              >
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <div>
                <DialogTitle className="text-xl font-bold">
                  {uploadTypes.find(t => t.key === selectedType)?.title} Upload
                </DialogTitle>
                <p className="text-muted-foreground">
                  {selectedType === 'text' && 'Share your written content with the community'}
                  {selectedType === 'audio' && 'Upload audio recordings for the corpus'}
                  {selectedType === 'video' && 'Share video content with the community'}
                  {selectedType === 'image' && 'Share images and visual content'}
                </p>
              </div>
            </DialogHeader>

            <Form {...form}>
              <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <FormField
                  control={form.control}
                  name="title"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Title</FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          placeholder={`Enter ${selectedType} title`}
                          data-testid="input-title"
                          className="bg-input border-border"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {selectedType !== 'text' && (
                  <FormField
                    control={form.control}
                    name="file"
                    render={({ field: { onChange, value, ...field } }) => (
                      <FormItem>
                        <FormLabel>
                          {selectedType === 'audio' && 'Audio File'}
                          {selectedType === 'video' && 'Video File'}
                          {selectedType === 'image' && 'Image Files'}
                        </FormLabel>
                        <FormControl>
                          <div className={`border-2 border-dashed border-border rounded-lg p-8 text-center transition-colors ${
                            selectedType === 'audio' ? 'hover:border-secondary' :
                            selectedType === 'video' ? 'hover:border-accent' : 'hover:border-muted'
                          }`}>
                            <CloudUpload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                            <p className="text-card-foreground font-medium mb-2">
                              Drop your {selectedType} file{selectedType === 'image' ? 's' : ''} here
                            </p>
                            <p className="text-muted-foreground text-sm mb-4">
                              {selectedType === 'audio' && 'or click to browse (MP3, WAV, OGG up to 100MB)'}
                              {selectedType === 'video' && 'or click to browse (MP4, AVI, MOV up to 500MB)'}
                              {selectedType === 'image' && 'or click to browse (JPEG, PNG, GIF up to 10MB each)'}
                            </p>
                            <Input
                              {...field}
                              type="file"
                              accept={
                                selectedType === 'audio' ? 'audio/*' :
                                selectedType === 'video' ? 'video/*' : 'image/*'
                              }
                              multiple={selectedType === 'image'}
                              onChange={(e) => {
                                const file = e.target.files?.[0];
                                onChange(file);
                              }}
                              data-testid="input-file"
                              className="hidden"
                              id="file-upload"
                            />
                            <Button
                              type="button"
                              variant="secondary"
                              onClick={() => document.getElementById('file-upload')?.click()}
                              data-testid="button-choose-file"
                            >
                              Choose File{selectedType === 'image' ? 's' : ''}
                            </Button>
                          </div>
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                )}

                {selectedType === 'text' && (
                  <FormField
                    control={form.control}
                    name="content"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Content</FormLabel>
                        <FormControl>
                          <Textarea
                            {...field}
                            rows={8}
                            placeholder="Enter your text content here..."
                            data-testid="textarea-content"
                            className="bg-input border-border"
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                )}

                <div className="grid grid-cols-2 gap-4">
                  <FormField
                    control={form.control}
                    name="category"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Category</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger data-testid="select-category" className="bg-input border-border">
                              <SelectValue placeholder="Select category" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            {selectedType === 'text' && (
                              <>
                                <SelectItem value="literature">Literature</SelectItem>
                                <SelectItem value="news">News</SelectItem>
                                <SelectItem value="educational">Educational</SelectItem>
                                <SelectItem value="poetry">Poetry</SelectItem>
                                <SelectItem value="translation">Translation</SelectItem>
                              </>
                            )}
                            {selectedType === 'audio' && (
                              <>
                                <SelectItem value="educational">Educational</SelectItem>
                                <SelectItem value="music">Music</SelectItem>
                                <SelectItem value="speech">Speech</SelectItem>
                                <SelectItem value="pronunciation">Pronunciation</SelectItem>
                              </>
                            )}
                            {selectedType === 'video' && (
                              <>
                                <SelectItem value="educational">Educational</SelectItem>
                                <SelectItem value="documentary">Documentary</SelectItem>
                                <SelectItem value="interview">Interview</SelectItem>
                                <SelectItem value="cultural">Cultural</SelectItem>
                                <SelectItem value="tutorial">Tutorial</SelectItem>
                              </>
                            )}
                            {selectedType === 'image' && (
                              <>
                                <SelectItem value="cultural">Cultural</SelectItem>
                                <SelectItem value="historical">Historical</SelectItem>
                                <SelectItem value="educational">Educational</SelectItem>
                                <SelectItem value="artistic">Artistic</SelectItem>
                                <SelectItem value="documentary">Documentary</SelectItem>
                              </>
                            )}
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />

                  <FormField
                    control={form.control}
                    name="language"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Language</FormLabel>
                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                          <FormControl>
                            <SelectTrigger data-testid="select-language" className="bg-input border-border">
                              <SelectValue placeholder="Select language" />
                            </SelectTrigger>
                          </FormControl>
                          <SelectContent>
                            <SelectItem value="telugu">Telugu</SelectItem>
                            <SelectItem value="hindi">Hindi</SelectItem>
                            <SelectItem value="english">English</SelectItem>
                            <SelectItem value="tamil">Tamil</SelectItem>
                            <SelectItem value="other">Other</SelectItem>
                          </SelectContent>
                        </Select>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>

                <FormField
                  control={form.control}
                  name="description"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Description</FormLabel>
                      <FormControl>
                        <Textarea
                          {...field}
                          rows={4}
                          placeholder={`Describe the ${selectedType} content...`}
                          data-testid="textarea-description"
                          className="bg-input border-border"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {selectedType === 'image' && (
                  <FormField
                    control={form.control}
                    name="tags"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Tags</FormLabel>
                        <FormControl>
                          <Input
                            {...field}
                            placeholder="Enter tags (comma-separated)"
                            data-testid="input-tags"
                            className="bg-input border-border"
                            onChange={(e) => field.onChange(e.target.value.split(',').map(tag => tag.trim()))}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                )}

                {isUploading && (
                  <div className="space-y-2">
                    <Progress value={uploadProgress} className="w-full" />
                    <p className="text-sm text-muted-foreground text-center">
                      Uploading... {Math.round(uploadProgress)}%
                    </p>
                  </div>
                )}

                <div className="flex space-x-4 pt-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={resetModal}
                    disabled={isUploading}
                    data-testid="button-cancel"
                    className="flex-1"
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={isUploading}
                    data-testid="button-upload"
                    className={`flex-1 ${
                      selectedType === 'text' ? 'bg-primary hover:bg-primary/90' :
                      selectedType === 'audio' ? 'bg-secondary hover:bg-secondary/90' :
                      selectedType === 'video' ? 'bg-accent hover:bg-accent/90' :
                      'bg-muted hover:bg-muted/90'
                    } text-white`}
                  >
                    {isUploading ? (
                      <>
                        <Upload className="mr-2 h-4 w-4 animate-pulse" />
                        Uploading...
                      </>
                    ) : (
                      <>
                        Upload {uploadTypes.find(t => t.key === selectedType)?.title.split(' ')[0]}
                      </>
                    )}
                  </Button>
                </div>
              </form>
            </Form>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}
