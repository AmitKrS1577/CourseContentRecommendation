export interface CourseItem {
  course_title: string;
  url: string;
  description: string;
}

export interface Recommendation {
  path_name: string;
  score: string;
  rationale: string;
  courses: CourseItem[];
}
