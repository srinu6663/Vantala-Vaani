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
  const { showNotification } = useNotification();
  const queryClient = useQueryClient();

  const [selectedType, setSelectedType] = useState<UploadType | null>(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);

  const form = useForm<UploadFormData>({
    resolver: zodResolver(uploadFormSchema),
    defaultValues: {
      title: "",
      description: "",
      content: "",
      category: "833299f6-ff1c-4fde-804f-6d3b3877c76e",
    },
  });

  // The useMutation is not directly used by the new onSubmit logic,
  // but we'll leave it in case you want to use it for other purposes.
  const uploadMutation = useMutation({
    mutationFn: ({ formData }: { formData: FormData }) => {
      return uploadRecord(formData);
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
    if (!userId) {
      showNotification('Error', 'User not identified. Cannot start upload.', 'error');
      return;
    }

    setIsUploading(true);
    setUploadProgress(5);

    try {
      let fileToUpload: File | undefined = data.file;
      let fileName: string;

      if (selectedType === 'text') {
        if (!data.content || data.content.trim() === '') throw new Error('No text content provided.');
        fileToUpload = new File([data.content], `${data.title.replace(/\s+/g, '-') || 'text-content'}.txt`, { type: 'text/plain' });
        fileName = fileToUpload.name;
      } else {
        if (!fileToUpload) throw new Error('No file selected.');
        fileName = fileToUpload.name;
      }

      const { uploadUuid, totalChunks } = await uploadFileInChunks(fileToUpload, setUploadProgress);

      const finalizeData = new URLSearchParams();
      finalizeData.append('title', data.title);
      if (data.description) finalizeData.append('description', data.description);
      finalizeData.append('category_id', '833299f6-ff1c-4fde-804f-6d3b3877c76e');
      finalizeData.append('user_id', userId);
      finalizeData.append('media_type', selectedType!);
      finalizeData.append('upload_uuid', uploadUuid);
      finalizeData.append('filename', fileName);
      finalizeData.append('total_chunks', totalChunks.toString());
      finalizeData.append('release_rights', 'creator');
      finalizeData.append('language', data.language || '');
      finalizeData.append('use_uid_filename', 'false');

      const resp = await fetch('https://api.corpus.swecha.org/api/v1/records/upload', {
        method: 'POST',
        headers: {
          ...(localStorage.getItem('authToken') ? { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` } : {}),
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: finalizeData.toString(),
      });

      if (!resp.ok) {
        const errText = await resp.text();
        try {
          const errJson = JSON.parse(errText);
          throw new Error(errJson.detail || 'Finalizing upload failed');
        } catch {
          throw new Error(errText || 'Finalizing upload failed');
        }
      }

      setUploadProgress(100);
      showNotification('Success', 'Content uploaded successfully!', 'success');

      setTimeout(() => {
        queryClient.invalidateQueries({ queryKey: ['/api/v1/users', userId, 'contributions'] });
        resetModal();
      }, 1200);

    } catch (err: any) {
      console.error("Upload process failed:", err);
      showNotification('Error', err.message || 'An unexpected error occurred', 'error');
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const uploadFileInChunks = async (file: File, onProgress: (percent: number) => void) => {
    const CHUNK_SIZE = 5 * 1024 * 1024;
    const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
    const uploadUuid = window.crypto.randomUUID();

    for (let i = 0; i < totalChunks; i++) {
      const start = i * CHUNK_SIZE;
      const end = Math.min(file.size, start + CHUNK_SIZE);
      const chunkBlob = file.slice(start, end);
      const chunkForm = new FormData();

      chunkForm.append('chunk', chunkBlob);
      chunkForm.append('filename', file.name);
      chunkForm.append('chunk_index', String(i));
      chunkForm.append('total_chunks', String(totalChunks));
      chunkForm.append('upload_uuid', uploadUuid);

      let success = false;
      let lastError: any = null;
      for (let attempt = 1; attempt <= 3; attempt++) {
        try {
          const resp = await fetch('https://api.corpus.swecha.org/api/v1/records/upload/chunk', {
            method: 'POST',
            headers: localStorage.getItem('authToken') ? { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` } : undefined,
            body: chunkForm
          });
          if (resp.ok) {
            success = true;
            break;
          } else {
            lastError = await resp.text();
          }
        } catch (err) {
          lastError = err;
        }
        await new Promise(res => setTimeout(res, 500 * attempt));
      }

      if (!success) {
        console.error("Chunk upload failed:", lastError);
        throw new Error(`Chunk upload failed: ${lastError}`);
      }
      onProgress(Math.round(((i + 1) / totalChunks) * 100));
    }
    return { uploadUuid, totalChunks };
  };

  const uploadTypes = [
    { key: 'text' as const, title: 'Text Content', description: 'Articles, stories, translations', icon: FileText, color: 'text-primary', bgColor: 'bg-primary/10 group-hover:bg-primary/20', borderColor: 'hover:border-primary hover:bg-primary/5' },
    { key: 'audio' as const, title: 'Audio Recording', description: 'Voice, music, pronunciation', icon: Mic, color: 'text-secondary', bgColor: 'bg-secondary/10 group-hover:bg-secondary/20', borderColor: 'hover:border-secondary hover:bg-secondary/5' },
    { key: 'video' as const, title: 'Video Content', description: 'Clips, interviews, lessons', icon: Video, color: 'text-accent', bgColor: 'bg-accent/10 group-hover:bg-accent/20', borderColor: 'hover:border-accent hover:bg-accent/5' },
    { key: 'image' as const, title: 'Image', description: 'Photos, illustrations, diagrams', icon: Images, color: 'text-muted-foreground', bgColor: 'bg-muted/10 group-hover:bg-muted/20', borderColor: 'hover:border-muted hover:bg-muted/5' },
  ];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto" aria-describedby="upload-dialog-description">
        {!selectedType ? (
          <>
            <DialogHeader>
              <DialogTitle className="text-2xl font-bold">New Contribution</DialogTitle>
              <p className="text-muted-foreground" id="upload-dialog-description">Choose the type of content you want to contribute</p>
            </DialogHeader>
            <div className="grid grid-cols-2 gap-4 py-4">
              {uploadTypes.map((type) => (
                <Button key={type.key} variant="outline" className={`p-6 h-auto flex-col space-y-3 group ${type.borderColor} transition-all`} onClick={() => { setSelectedType(type.key); form.setValue('type', type.key); }} data-testid={`upload-type-${type.key}`}>
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
          <>
            <DialogHeader className="flex flex-row items-center space-y-0 space-x-4">
              <Button variant="ghost" size="sm" onClick={() => setSelectedType(null)} data-testid="button-back" className="text-muted-foreground hover:text-foreground">
                <ArrowLeft className="h-4 w-4" />
              </Button>
              <div>
                <DialogTitle className="text-xl font-bold">{uploadTypes.find(t => t.key === selectedType)?.title} Upload</DialogTitle>
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
                <FormField control={form.control} name="title" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Title</FormLabel>
                    <FormControl>
                      <Input {...field} placeholder={`Enter ${selectedType} title`} data-testid="input-title" className="bg-input border-border" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )} />

                {/* --- THIS IS THE FIX --- */}
                {/* Show this field only for text uploads */}
                {selectedType === 'text' && (
                  <FormField control={form.control} name="content" render={({ field }) => (
                    <FormItem>
                      <FormLabel>Content</FormLabel>
                      <FormControl>
                        <Textarea {...field} value={field.value ?? ""} rows={8} placeholder="Type your article, story, or text content here..." data-testid="textarea-content" className="bg-input border-border" />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )} />
                )}
                {/* -------------------- */}

                {/* Show this field for all types EXCEPT text */}
                {selectedType !== 'text' && (
                  <FormField control={form.control} name="file" render={({ field: { onChange, value, ...field } }) => (
                    <FormItem>
                      <FormLabel>{selectedType === 'audio' && 'Audio File'}{selectedType === 'video' && 'Video File'}{selectedType === 'image' && 'Image File'}</FormLabel>
                      <FormControl>
                        <div className={`border-2 border-dashed border-border rounded-lg p-8 text-center transition-colors ${selectedType === 'audio' ? 'hover:border-secondary' : selectedType === 'video' ? 'hover:border-accent' : 'hover:border-muted'}`}>
                          <CloudUpload className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                          <p className="text-card-foreground font-medium mb-2">Drop your {selectedType} file here</p>
                          <p className="text-muted-foreground text-sm mb-4">
                            {selectedType === 'audio' && 'or click to browse (MP3, WAV, OGG up to 100MB)'}
                            {selectedType === 'video' && 'or click to browse (MP4, AVI, MOV up to 500MB)'}
                            {selectedType === 'image' && 'or click to browse (JPEG, PNG, GIF up to 10MB each)'}
                          </p>
                          <Input {...field} type="file" accept={selectedType === 'audio' ? 'audio/*' : selectedType === 'video' ? 'video/*' : 'image/*'} onChange={(e) => { const file = e.target.files?.[0]; onChange(file); }} data-testid="input-file" className="hidden" id="file-upload" />
                          <Button type="button" variant="secondary" onClick={() => document.getElementById('file-upload')?.click()} data-testid="button-choose-file">Choose File</Button>
                          {value && value.name && (
                            <div className="mt-4 text-left text-sm bg-muted/30 rounded p-2">
                              <div><b>File:</b> {value.name}</div>
                              <div><b>Size:</b> {(value.size / 1024 / 1024).toFixed(2)} MB</div>
                              <div><b>Type:</b> {value.type}</div>
                            </div>
                          )}
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )} />
                )}

                <FormField control={form.control} name="language" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Language</FormLabel>
                    <Select onValueChange={field.onChange} defaultValue={field.value ?? ''}>
                      <FormControl>
                        <SelectTrigger data-testid="select-language" className="bg-input border-border">
                          <SelectValue placeholder="Select language" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="telugu">Telugu</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )} />

                <FormField control={form.control} name="description" render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea {...field} value={field.value ?? ''} rows={4} placeholder={`Describe the ${selectedType} content...`} data-testid="textarea-description" className="bg-input border-border" />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )} />

                <div className="flex space-x-4 pt-4">
                  <Button type="button" variant="outline" onClick={resetModal} disabled={isUploading} data-testid="button-cancel" className="flex-1">Cancel</Button>
                  <Button type="submit" disabled={isUploading} data-testid="button-upload" className={`flex-1 ${selectedType === 'text' ? 'bg-primary hover:bg-primary/90' : selectedType === 'audio' ? 'bg-secondary hover:bg-secondary/90' : selectedType === 'video' ? 'bg-accent hover:bg-accent/90' : 'bg-muted hover:bg-muted/90'} text-white`}>
                    {isUploading ? (
                      <><Upload className="mr-2 h-4 w-4 animate-pulse" />Uploading...</>
                    ) : (
                      <>Upload {uploadTypes.find(t => t.key === selectedType)?.title.split(' ')[0]}</>
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